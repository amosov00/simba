from typing import List, Optional, Union

from bson import ObjectId

from config import SST_CONTRACT
from database.crud import UserCRUD, ReferralCRUD, EthereumTransactionCRUD, InvoiceCRUD
from schemas import (
    User, InvoiceInDB, EthereumTransactionInDB, ReferralTransactionEmail, ObjectIdPydantic, SSTContractEvents
)

__all__ = ["ReferralMechanics"]


class ReferralMechanics:
    def __init__(self, user: User):
        if isinstance(user, dict):
            user = User(**user)

        self.user = user
        assert user is not None, "user must be set"
        self.referral_object: dict = {}
        self.referrals: List[dict] = []
        self.referrals_transactions: List[dict] = []

    async def _fetch_referral_object(self):
        if not self.referral_object:
            self.referral_object = await ReferralCRUD.find_by_user_id(self.user.id)

        return self.referral_object

    @staticmethod
    def get_user_level_from_referral_object(
        user_id: Union[ObjectId, ObjectIdPydantic], referral_object: dict
    ) -> Optional[int]:

        if not referral_object:
            return None

        for key, val in referral_object.items():
            if key.startswith("ref") and val == user_id:
                return int(key[-1])

        return None

    async def _parse_sst_txs_with_user(self) -> list:
        parsed_txs = []

        for tx in self.referrals_transactions:
            tx = EthereumTransactionInDB(**tx)
            receiver_wallet_hash = tx.args.get("to", "").lower()
            sst_transfered = tx.args.get("value")

            for user in self.referrals:
                if tx.user_id and tx.user_id == user["_id"]:
                    parsed_txs.append(
                        {
                            "transactionHash": tx.transactionHash,
                            "amount": sst_transfered,
                            "level": user.get("level"),
                            "user_id": tx.user_id,
                        }
                    )
                elif receiver_wallet_hash in (i.get("address", "").lower() for i in user["user_eth_addresses"]):
                    parsed_txs.append(
                        {
                            "transactionHash": tx.transactionHash,
                            "amount": sst_transfered,
                            "level": user.get("level"),
                            "user_id": user.get("_id"),
                        }
                    )

        return parsed_txs

    @classmethod
    async def fetch_ref_txs_info_from_invoice(cls, invoice: InvoiceInDB) -> list:
        sst_txs = await EthereumTransactionCRUD.find_many(
            {
                "contract": SST_CONTRACT.title,
                "event": SSTContractEvents.Transfer,
                "$or": [{"transactionHash": {"$in": invoice.sst_tx_hashes}}, {"invoice_id": invoice.id}],
            }
        )

        if not sst_txs:
            return []

        user = User(**await UserCRUD.find_by_id(invoice.user_id, raise_404=True))

        self = cls(user)
        self.referrals_transactions.extend(sst_txs)
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
        """Поиск приглашенных рефералов сверху вниз по вершинам."""
        for ref_level in range(1, 6):
            ref_objects = await ReferralCRUD.find_many({f"ref{ref_level}": self.user.id})
            users_ids = [i["user_id"] for i in ref_objects]

            if users_ids:
                users = await UserCRUD.aggregate(
                    [
                        {"$match": {"_id": {"$in": users_ids}}},
                        {"$addFields": {"referral_level": ref_level}},
                    ]
                )
                self.referrals.extend(users)

        return self.referrals

    async def fetch_sst_tx_info_for_user(self, transactions: List[dict]) -> list:
        """Поиск информации (уровень, сумма и почта связанного юзера) по SST
        транзакциям."""
        resp = []

        for transaction in transactions:
            transaction = EthereumTransactionInDB(**transaction)
            amount = transaction.args.get("value")
            invoice = await InvoiceCRUD.find_by_id(transaction.invoice_id)

            if not invoice:
                resp.append(ReferralTransactionEmail(transactionHash=transaction.transactionHash, amount=amount))
                continue

            connected_user = await UserCRUD.find_by_id(invoice["user_id"])
            connected_user_ref_object = await ReferralCRUD.find_by_user_id(connected_user["_id"])

            resp.append(
                ReferralTransactionEmail(
                    transactionHash=transaction.transactionHash,
                    amount=amount,
                    email=connected_user.get("email"),
                    level=self.get_user_level_from_referral_object(self.user.id, connected_user_ref_object),
                )
            )

        return resp
