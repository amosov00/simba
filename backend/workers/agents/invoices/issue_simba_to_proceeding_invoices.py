import asyncio
import logging
from datetime import timedelta

from sentry_sdk import capture_exception

from core.mechanics import InvoiceMechanics
from database.crud import InvoiceCRUD, UserCRUD, MetaCRUD
from schemas import InvoiceInDB, InvoiceStatus, InvoiceType, MetaSlugs, BTCTransaction
from workers.agents import app

__all__ = ["issue_simba_to_proceeding_invoices_job"]

issue_simba_to_proceeding_invoices_topic = app.topic(
    "issue_simba_to_proceeding_invoices", internal=True, retention=timedelta(minutes=10), partitions=1
)


@app.agent(issue_simba_to_proceeding_invoices_topic, concurrency=1)
async def issue_simba_to_proceeding_invoices_job(stream):
    """Cron for sending SIMBA for buy invoice with PROCESSING status"""

    async for _ in stream:
        meta_manual_payout = await MetaCRUD.find_by_slug(MetaSlugs.MANUAL_PAYOUT)
        # Finish pipeline if manual mode
        if meta_manual_payout["payload"]["is_active"] is True:
            continue

        proceeding_invoices = await InvoiceCRUD.find_with_txs(
            match_query={
                "invoice_type": InvoiceType.BUY,
                "status": InvoiceStatus.PROCESSING,
                "eth_tx_hashes": [],
                "simba_amount_proceeded": 0,
            },
            fetch_btc=True,
            fetch_eth=False,
        )

        for invoice in proceeding_invoices:
            btc_txs = invoice.pop("btc_txs")
            invoice = InvoiceInDB(**invoice)

            if not btc_txs:
                logging.error(f"Failed to related btc txs for invoice {invoice.id}, skipping")
                continue

            btc_txs = list(filter(lambda o: o.get("simba_tokens_issued") is False, btc_txs))

            if not btc_txs:
                logging.error(f"Failed to find unissued btc tx for invoice {invoice.id}, skipping")
                continue

            user = await UserCRUD.find_by_id(invoice.user_id)

            try:
                await InvoiceMechanics(invoice, user).issue_simba_tokens(transaction=BTCTransaction(**btc_txs[0]))
            except Exception as e:
                logging.exception(e)
                capture_exception(e)
                continue

            # Wait for ethereum blockchain (nonce and etc)
            await asyncio.sleep(3)

    return
