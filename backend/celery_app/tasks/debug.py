import asyncio
from datetime import datetime

from database.crud import DebugCRUD
from celery_app import celery_instance

__all__ = ['debug_task_1']


# async def debug_task_1_coro():
#     await DebugCRUD.insert_one({"created_at": datetime.now(), "payload": "Hello from debug_task_1"})
#     return None


@celery_instance.task
async def debug_task_1():
    print('Hello there')
    await DebugCRUD.insert_one({"created_at": datetime.now(), "payload": "Hello from debug_task_1 New"})
    return None
