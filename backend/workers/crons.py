from workers.agents import (
    delete_unused_webhooks_job,
    finish_overdue_invoices_job,
    rescue_stucked_invoices_job,
    send_btc_to_proceeding_invoices_job,
    fetch_and_proceed_simba_contract_job,
    fetch_simba_meta_job,
    fetch_and_proceed_sst_contract_job,
    update_btc_addresses_info_job,
    update_empty_btc_addresses_info_job,
    double_check_contracts_job,
    update_blacklisted_balance_job,
)

from workers.app import get_faust_app

app = get_faust_app()


@app.crontab("*/1 * * * *")
async def finish_overdue_invoices_cron():
    await finish_overdue_invoices_job.cast()


@app.crontab("*/1 * * * *")
async def fetch_and_proceed_simba_contract_cron():
    await fetch_and_proceed_simba_contract_job.cast()


@app.crontab("5 */1 * * *")
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


@app.crontab("30 */1 * * *")
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


@app.crontab("15 */12 * * *")
async def update_blacklisted_balance_cron():
    await update_blacklisted_balance_job.cast()