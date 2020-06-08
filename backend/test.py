from asyncio import get_event_loop

from celery_app.tasks import debug_task_1


async def main():
    await debug_task_1.delay()

if __name__ == '__main__':
    # debug_task_1.delay()
    loop = get_event_loop()
    loop.run_until_complete(main())
