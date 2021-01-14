from celery_app.celeryconfig import app

__all__ = ["update_single_btc_address_info"]


@app.task(
    name="update_single_btc_address_info",
    bind=True,
    retry_backoff=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5},
)
async def update_single_btc_address_info(self, wallet_address: str, *args, **kwargs):
    # logging.info(f"Updated BTC wallet {wallet_address}")
    return True
