from workers.agents import *

from workers.app import get_faust_app

app = get_faust_app()


@app.crontab("*/1 * * * *")
async def finish_overdue_invoices_cron():
    await finish_overdue_invoices_job.cast()


@app.crontab("*/1 * * * *")
async def fetch_and_proceed_simba_contract_cron():
    await fetch_and_proceed_simba_contract_job.cast()


@app.crontab("*/15 * * *")
async def fetch_simba_meta_cron():
    await fetch_simba_meta_job.cast()


@app.crontab("*/2 * * * *")
async def send_btc_to_proceeding_invoices_cron():
    await send_btc_to_proceeding_invoices_job.cast()


@app.crontab("20 */3 * * *")
async def delete_unused_webhooks_cron():
    await delete_unused_webhooks_job.cast()


@app.crontab("20 */1 * * *")
async def rescue_stucked_invoices_cron():
    await rescue_stucked_invoices_job.cast()


@app.crontab("*/5 * * * *")
async def fetch_and_proceed_sst_contract_cron():
    await fetch_and_proceed_sst_contract_job.cast()


@app.crontab("0 2 * * *")
async def update_btc_addresses_info_cron():
    await update_btc_addresses_info_job.cast()


@app.crontab("0 */12 * * *")
async def update_empty_btc_addresses_info_cron():
    await update_empty_btc_addresses_info_job.cast()


@app.crontab("10 */12 * * *")
async def double_check_contracts_cron():
    await double_check_contracts_job.cast()


@app.crontab("15 */6 * * *")
async def update_blacklisted_balance_cron():
    await update_blacklisted_balance_job.cast()


@app.crontab("*/1 * * * *")
async def currency_rate_cron():
    await currency_rate_job.cast()
