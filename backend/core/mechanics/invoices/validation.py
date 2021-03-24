from config import (
    SIMBA_BUY_SELL_FEE,
    SIMBA_MINIMAL_BUY_AMOUNT,
)
from core.mechanics.crypto.base import CryptoValidation
from core.mechanics.user_kyc import KYCController
from database.crud import MetaCRUD
from schemas import (
    InvoiceType,
    InvoiceStatus,
    BTCTransaction,
    MetaSlugs,
    UserKYCVerificationLimit,
)
from .base import InvoiceBase


class InvoiceValidation(CryptoValidation, InvoiceBase):
    async def _validate_common(self):
        if not self.invoice.user_id:
            self.errors.append("`user_id` field is missing")
        if not self.invoice.target_btc_address:
            self.errors.append("bitcoin wallet address is required")
        if not self.invoice.target_eth_address:
            self.errors.append("ethereum wallet address is required")
        if not self.validate_simba_amount(self.invoice.simba_amount):
            self.errors.append(f"min simba token amount: {SIMBA_MINIMAL_BUY_AMOUNT}")
        if self.invoice.invoice_type not in (InvoiceType.SELL, InvoiceType.BUY):
            self.errors.append("invalid invoice type")

        await self._validate_verification_limits(
            btc_amount=self.invoice.btc_amount_proceeded
            if self.invoice.btc_amount_proceeded > 0
            else self.invoice.btc_amount
        )

        return None

    async def _validate_verification_limits(self, btc_amount: int = 0) -> UserKYCVerificationLimit:
        user_id = self.user.id if self.user else self.invoice.id

        verification_limit = await (await KYCController.init(user_id)).calculate_verification_limit(btc_amount)

        if not verification_limit.is_allowed:
            self.errors.append("verification limit exceeded")

        return verification_limit

    def _validate_for_buy(self):
        if not self.validate_currency_rate(
            self.invoice.invoice_type, self.invoice.btc_amount, self.invoice.simba_amount
        ):
            self.errors.append("invalid rate")
        if self.user:
            if not self.user.has_address("eth", self.invoice.target_eth_address):
                self.errors.append("user has no target_eth_address")
        return True

    def _validate_for_sell(self):
        if not self.validate_currency_rate(
            self.invoice.invoice_type, self.invoice.btc_amount, self.invoice.simba_amount
        ):
            self.errors.append("invalid rate")
        if self.user:
            if not self.user.has_address("eth", self.invoice.target_eth_address):
                self.errors.append("user has no target_eth_address")
            if not self.user.has_address("btc", self.invoice.target_btc_address):
                self.errors.append("user has no target_btc_address")
        return True

    def _validate_for_sending_btc(self):
        if not self.invoice.status == InvoiceStatus.PROCESSING:
            self.errors.append("invalid invoice status")
        if self.invoice.simba_amount_proceeded < SIMBA_MINIMAL_BUY_AMOUNT:
            self.errors.append("too low simba tokens value")
        if self.invoice.simba_amount_proceeded == self.invoice.btc_amount_proceeded + SIMBA_BUY_SELL_FEE:
            self.errors.append("btc are already sent")
        if self.invoice.btc_tx_hashes:
            self.errors.append("btc txs are already exist")

        self._raise_exception_if_exists()

        return True

    async def _validate_for_multisig(self):
        meta_manual_payout = await MetaCRUD.find_by_slug(MetaSlugs.MANUAL_PAYOUT)
        if meta_manual_payout["payload"]["is_active"] is False:
            self.errors.append("Payout mode is auto now")

        return True

    def _validate_transaction(self, tx: BTCTransaction):
        if self.invoice.target_btc_address not in tx.addresses:
            self.errors.append("Invalid target btc address")

        output_value = self.get_incoming_btc_from_outputs(tx.outputs, self.invoice.target_btc_address)

        if not output_value:
            self.errors.append("BTC output is not found")

        if self.invoice.invoice_type == InvoiceType.BUY and output_value != self.invoice.btc_amount_proceeded:
            self.errors.append("Invalid btc amount")

        if (
            self.invoice.invoice_type == InvoiceType.SELL
            and output_value != self.invoice.simba_amount_proceeded - SIMBA_BUY_SELL_FEE
        ):
            self.errors.append("Invalid btc amount")

        return True
