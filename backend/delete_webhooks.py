import asyncio

from celery_app.tasks import delete_unused_webhooks

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(delete_unused_webhooks())
