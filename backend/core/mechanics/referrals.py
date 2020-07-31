from typing import List

from database.crud import UserCRUD, ReferralCRUD, EthereumTransactionCRUD
from config import SST_CONTRACT
from schemas import User, InvoiceInDB, EthereumTransactionInDB

__all__ = ["ReferralMechanics"]


class ReferralMechanics:
    def __init__(self, user: User):
        self.user = user
        assert user is not None, "user must be set"
        self.referral_object: dict = dict()
        self.referrals: List[dict] = []
        self.referrals_transactions: List[dict] = []

    async def _fetch_referral_object(self):
        self.referral_object = await ReferralCRUD.find_by_user_id(self.user.id)
        return self.referral_object

    async def _parse_sst_txs_with_user(self) -> list:
        parsed_txs = []
        for tx in self.referrals_transactions:
            tx = EthereumTransactionInDB(**tx)
            receiver_wallet_hash = tx.args.get("to")
            sst_transfered = tx.args.get("value")

            for user in self.referrals:
                if tx.user_id:
                    if tx.user_id == user["_id"]:
                        parsed_txs.append({
                            "transactionHash": tx.transactionHash,
                            "amount": sst_transfered,
                            "level": user.get("level"),
                            "user_id": tx.user_id
                        })
                else:
                    eth_wallet_hashes = [i.get("address") for i in user["user_eth_addresses"]]
                    if receiver_wallet_hash in eth_wallet_hashes:
                        parsed_txs.append({
                            "transactionHash": tx.transactionHash,
                            "amount": sst_transfered,
                            "level": user.get("level"),
                            "user_id": user.get("_id")
                        })

        return parsed_txs

    @classmethod
    async def fetch_ref_txs_info_from_invoice(cls, invoice: InvoiceInDB) -> list:
        full_sst_txs = await EthereumTransactionCRUD.find_many({
            "contract": SST_CONTRACT.title, "transactionHash": {"$in": invoice.sst_tx_hashes}
        }) if invoice.sst_tx_hashes else None
        import logging;
        logging.debug(full_sst_txs)
        if not full_sst_txs:
            return []

        user = User(**await UserCRUD.find_by_id(invoice.user_id, raise_404=True))

        self = cls(user)
        self.referrals_transactions.extend(full_sst_txs)
        await self.fetch_referrals_from_ref_obj()

        return await self._parse_sst_txs_with_user()

    async def fetch_referrals_from_ref_obj(self):
        if not self.referral_object:
            await self._fetch_referral_object()

        for key, val in self.referral_object.items():
            if not val or not key.startswith("ref"):
                continue
            else:
                user = await UserCRUD.find_by_id(val)

                if user:
                    user["level"] = key[-1]
                    self.referrals.append(user)

        return self.referrals

    async def fetch_referrals_top_to_bottom(self) -> list:
        """
        Поиск приглашенных рефералов сверху вниз по вершинам
        :return:
        """
        for ref_level in range(1, 6):
            ref_objects = await ReferralCRUD.find_many({f"ref{ref_level}": self.user.id})
            users_ids = [i["user_id"] for i in ref_objects]

            if users_ids:
                users = await UserCRUD.aggregate(
                    [{"$match": {"_id": {"$in": users_ids}}}, {"$addFields": {"referral_level": ref_level}}, ]
                )
                self.referrals.extend(users)

        return self.referrals
