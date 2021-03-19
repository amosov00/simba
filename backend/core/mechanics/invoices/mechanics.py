import asyncio
from datetime import datetime
from http import HTTPStatus
from typing import Union

from fastapi import HTTPException
from sentry_sdk import capture_message

from config import (
    IS_PRODUCTION,
    SIMBA_BUY_SELL_FEE,
    TRANSACTION_MIN_CONFIRMATIONS,
    BTC_FEE,
    settings,
)
from core.mechanics.blockcypher_webhook import BlockCypherWebhookHandler
from core.mechanics.crypto import SimbaWrapper, SSTWrapper, BitcoinWrapper
from core.mechanics.invoices.validation import InvoiceValidation
from core.utils.email import Email
from database.crud import BTCTransactionCRUD, EthereumTransactionCRUD, UserCRUD
from schemas import (
    User,
    InvoiceInDB,
    InvoiceType,
    InvoiceStatus,
    EthereumTransaction,
    EthereumTransactionInDB,
    BTCTransaction,
    BTCTransactionInDB,
    SimbaContractEvents,
    BlockCypherWebhookEvents,
)

__all__ = ["InvoiceMechanics"]


class InvoiceMechanics(InvoiceValidation):
    async def validate(self, raise_exceprion: bool = True) -> bool:
        """Validate invoice, returns True if valid"""
        await self._validate_common()

        if self.invoice.invoice_type == InvoiceType.BUY:
            self._validate_for_buy()

        elif self.invoice.invoice_type == InvoiceType.SELL:
            self._validate_for_sell()

        if raise_exceprion:
            self._raise_exception_if_exists()

        return not bool(self.errors)

    async def _issue_simba_tokens_and_save(
        self,
        transaction: BTCTransaction,
        incoming_btc: int,
    ):
        self._raise_exception_if_exists()

        verification_limit_instance = await self._validate_verification_limits(incoming_btc)

        # check for kyc limits
        if verification_limit_instance.is_allowed:
            eth_tx_hash = await SimbaWrapper().issue_tokens(
                customer_address=self.invoice.target_eth_address,
                incoming_btc=incoming_btc,
                btc_tx_hash=transaction.hash,
                invoice=self.invoice,
            )
            transaction.simba_tokens_issued = True
            self.invoice.status = InvoiceStatus.PAID
            # Subtract fee
            self.invoice.simba_amount_proceeded += incoming_btc - SIMBA_BUY_SELL_FEE
            self.invoice.add_hash("eth", eth_tx_hash)

        else:
            eth_tx_hash = ""
            self.invoice.status = InvoiceStatus.SUSPENDED

        self.invoice.btc_amount_proceeded += incoming_btc
        self.invoice.add_hash("btc", transaction.hash)
        await BTCTransactionCRUD.update_or_insert({"hash": transaction.hash}, transaction.dict())
        await self.update_invoice()

        asyncio.create_task(BitcoinWrapper().fetch_address_and_save(self.invoice.target_btc_address))

        if not verification_limit_instance.is_allowed:
            user = User(**await UserCRUD.find_by_id(self.invoice.user_id))
            asyncio.create_task(SSTWrapper(self.invoice).send_sst_to_referrals(user, self.invoice.btc_amount))
            self._log(f"success simba tokens issue - tx hash {eth_tx_hash}")
        else:
            asyncio.create_task(Email().new_suspended_invoice(invoice=self.invoice))
            self._log(f"got suspended invoice (buy type): {self.invoice.id}")

        return True

    async def _proceed_new_btc_tx_buy(self, new_transaction: BTCTransaction, transaction_in_db: BTCTransactionInDB):
        """Part of buy pipeline."""
        incoming_btc = self.get_incoming_btc_from_outputs(new_transaction.outputs, self.invoice.target_btc_address)

        if not incoming_btc:
            capture_message("Failed to parse btc amount from transaction", level="error")
            self.errors.append("Failed to parse btc amount from transaction")
            self._raise_exception_if_exists()

        if all(
            [
                new_transaction.confirmations >= TRANSACTION_MIN_CONFIRMATIONS,
                transaction_in_db.simba_tokens_issued is False if transaction_in_db else True,
                self.invoice.status == InvoiceStatus.WAITING,
            ]
        ):
            self._log(f"issuing simba tokens - {incoming_btc}")
            return await self._issue_simba_tokens_and_save(new_transaction, incoming_btc)

        else:
            self._log("failed some conditions - save and skip")
            return await BTCTransactionCRUD.update_or_insert(
                {"hash": new_transaction.hash}, new_transaction.dict(exclude_unset=True)
            )

    async def _proceed_new_btc_tx_sell(self, new_transaction: BTCTransaction, transaction_in_db: BTCTransactionInDB):
        """Part of sell pipeline."""
        if all(
            [
                bool(new_transaction.block_height),
                new_transaction.confirmations >= TRANSACTION_MIN_CONFIRMATIONS,
                transaction_in_db.simba_tokens_issued is False if transaction_in_db else True,
                self.invoice.status == InvoiceStatus.PROCESSING,
            ]
        ):
            self.invoice.status = InvoiceStatus.COMPLETED
            self.invoice.finised_at = datetime.now()

            # send without fee cause of double fee charge
            btc_outcoming_without_fee = self.invoice.btc_amount_proceeded + SIMBA_BUY_SELL_FEE

            eth_tx_hash = await SimbaWrapper().redeem_tokens(
                btc_outcoming_without_fee, new_transaction.hash, invoice=self.invoice
            )
            self.invoice.add_hash("eth", eth_tx_hash)

            await self.update_invoice()
            await BTCTransactionCRUD.update_or_insert(
                {"hash": new_transaction.hash}, new_transaction.dict(exclude_unset=True)
            )

        else:
            await BTCTransactionCRUD.update_or_insert(
                {"hash": new_transaction.hash}, new_transaction.dict(exclude_unset=True)
            )

        return True

    async def proceed_new_btc_transaction(self, transaction: BTCTransaction):
        transaction.invoice_id = self.invoice.id

        if transaction_in_db := await BTCTransactionCRUD.find_one({"hash": transaction.hash}):
            transaction_in_db = BTCTransactionInDB(**transaction_in_db)
            self._log(f"find transaction_in_db (id {transaction_in_db.id})")

        self._raise_exception_if_exists()

        if self.invoice.invoice_type == InvoiceType.BUY:
            return await self._proceed_new_btc_tx_buy(transaction, transaction_in_db)

        elif self.invoice.invoice_type == InvoiceType.SELL:
            return await self._proceed_new_btc_tx_sell(transaction, transaction_in_db)

        return True

    async def _proceed_new_eth_tx_transfer(self, transaction: EthereumTransactionInDB):
        """Part of sell pipeline."""
        incoming_eth = self.get_incoming_simba(transaction)

        if not incoming_eth:
            capture_message("failed to parse incoming eth from transaction", level="error")
            self.errors.append("failed to parse incoming eth from transaction")

        self._raise_exception_if_exists()

        transaction.invoice_id = self.invoice.id

        verification_limit_instance = await self._validate_verification_limits(incoming_eth)

        if verification_limit_instance.is_allowed:
            if self.invoice.invoice_type == InvoiceType.SELL and self.invoice.status == InvoiceStatus.WAITING:
                self.invoice.status = InvoiceStatus.PROCESSING
                self.invoice.simba_amount_proceeded = incoming_eth

        else:
            self.invoice.status = InvoiceStatus.SUSPENDED
            self.invoice.simba_amount_proceeded = incoming_eth

        await EthereumTransactionCRUD.update_one(
            {"_id": transaction.id}, transaction.dict(exclude={"id"}, exclude_unset=True)
        )
        self.invoice.add_hash("eth", transaction.transactionHash)
        await self.update_invoice()

        if verification_limit_instance.is_allowed:
            self._log(f"confirmed simba tokens transfer - tx hash {transaction.transactionHash}")
        else:
            asyncio.create_task(Email().new_suspended_invoice(invoice=self.invoice))
            self._log(f"got suspended invoice (sell type): {self.invoice.id}")

        return True

    async def _proceed_new_eth_tx_issue_redeem(self, transaction: EthereumTransactionInDB):
        """Part of buy and sell pipeline, just for adding extra info in
        invoice."""
        transaction.invoice_id = self.invoice.id
        self.invoice.add_hash("eth", transaction.transactionHash)

        if transaction.event == SimbaContractEvents.OnIssued and self.invoice.status == InvoiceStatus.PAID:
            self.invoice.status = InvoiceStatus.COMPLETED
            self.invoice.finised_at = datetime.now()

        await EthereumTransactionCRUD.update_one(
            {"_id": transaction.id}, transaction.dict(exclude={"id"}, exclude_unset=True)
        )
        await self.update_invoice()
        self._log(f"confirmed simba tokens issue or redeemed - tx hash {transaction.transactionHash}")
        return True

    async def proceed_new_eth_transaction(self, transaction: EthereumTransactionInDB):
        if transaction.event == SimbaContractEvents.Transfer:
            return await self._proceed_new_eth_tx_transfer(transaction)
        elif transaction.event in (SimbaContractEvents.OnRedeemed, SimbaContractEvents.OnIssued):
            return await self._proceed_new_eth_tx_issue_redeem(transaction)
        else:
            capture_message("Unindentified invoice type", level="warning")
        return True

    async def proceed_new_transaction(
        self, transaction: Union[BTCTransaction, EthereumTransaction]
    ) -> Union[bool, str]:
        if isinstance(transaction, (BTCTransaction, BTCTransactionInDB)):
            self._log(f"new BTC transaction: {transaction.hash}")
            return await self.proceed_new_btc_transaction(transaction)
        elif isinstance(transaction, (EthereumTransaction, EthereumTransactionInDB)):
            self._log(f"new ETH transaction: {transaction.transactionHash}")
            return await self.proceed_new_eth_transaction(transaction)
        else:
            self._log(f"unknown type of tx: {type(transaction)}", "error")

    async def send_bitcoins(self):
        self._validate_for_sending_btc()

        btc_outcoming_without_fee = self.invoice.simba_amount_proceeded
        btc_outcoming_with_fee = btc_outcoming_without_fee - SIMBA_BUY_SELL_FEE

        verification_limit_instance = await self._validate_verification_limits(btc_outcoming_with_fee)

        if not verification_limit_instance.is_allowed:
            self.invoice.status = InvoiceStatus.SUSPENDED
            await self.update_invoice()
            self._log(f"got suspended invoice (sell type): {self.invoice.id}")
            return False

        btc_tx = await BitcoinWrapper().create_and_sign_transaction(
            address=self.invoice.target_btc_address, amount=btc_outcoming_with_fee
        )
        if not btc_tx:
            capture_message(f"failed to get btc tx info from invoice {self.invoice.id}", level="error")
            return False

        btc_tx.invoice_id = self.invoice.id
        self.invoice.btc_amount_proceeded = btc_outcoming_with_fee
        self.invoice.add_hash("btc", btc_tx.hash)

        await BTCTransactionCRUD.insert_one(btc_tx.dict())
        await self.update_invoice()

        asyncio.create_task(
            BlockCypherWebhookHandler().create_webhook(
                invoice=self.invoice,
                event=BlockCypherWebhookEvents.TX_CONFIMATION,
                transaction_hash=btc_tx.hash,
            )
        )
        return True

    async def fetch_multisig_transaction_data(self):
        """Fetch data for cosigner 1."""
        await self.validate()
        await self._validate_for_multisig()
        self._raise_exception_if_exists()

        multisig_wallet = await BitcoinWrapper().fetch_address_and_save(settings.crypto.btc_multisig_wallet_address)

        if multisig_wallet.unconfirmed_transactions_number != 0:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "wallet has outcoming transations")

        if self.invoice.simba_amount_proceeded >= multisig_wallet.balance:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "not enough balance to pay")

        spendables = await BitcoinWrapper().blockcypher_api_wrapper.get_spendables(
            settings.crypto.btc_multisig_wallet_address
        )
        payables = [(self.invoice.target_btc_address, self.invoice.simba_amount_proceeded - SIMBA_BUY_SELL_FEE)]
        return {
            "cosig1Priv": settings.crypto.btc_multisig_cosig_1_wif,
            "cosig2Pub": settings.crypto.btc_multisig_cosig_2_pub,
            "spendables": spendables,
            "payables": payables,
            "fee": BTC_FEE,
            "testnet": not IS_PRODUCTION,
        }

    async def proceed_multisig_transaction(self, transaction_hash: str) -> InvoiceInDB:
        bitcoin_wrapper = BitcoinWrapper()
        decoded_tx = await bitcoin_wrapper.blockcypher_api_wrapper.decode_tx(transaction_hash)

        # validate decoded
        self._validate_transaction(decoded_tx)
        self._raise_exception_if_exists()

        pushed_tx = await bitcoin_wrapper.blockcypher_api_wrapper.push_raw_tx(transaction_hash)

        self.invoice.btc_amount_proceeded = self.get_incoming_btc_from_outputs(
            pushed_tx.outputs, self.invoice.target_btc_address
        )
        if not self.invoice.btc_amount_proceeded:
            capture_message(f"Invalid btc amount data in TX {pushed_tx.hash}", level="error")
            raise HTTPException(HTTPStatus.BAD_REQUEST, "Invalid btc amount data")

        self.invoice.add_hash("btc", pushed_tx.hash)
        pushed_tx.invoice_id = self.invoice.id

        await BTCTransactionCRUD.insert_one(pushed_tx.dict())
        await self.update_invoice()

        asyncio.create_task(
            BlockCypherWebhookHandler().create_webhook(
                invoice=self.invoice,
                event=BlockCypherWebhookEvents.TX_CONFIMATION,
                transaction_hash=pushed_tx.hash,
            )
        )

        return self.invoice
