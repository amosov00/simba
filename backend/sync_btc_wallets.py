import asyncio
from celery_app.tasks import update_empty_btc_addresses_info

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_empty_btc_addresses_info())