from celery_app.celeryconfig import app

__all__ = ['debug_task_1']

INC_LIST = [0, ]


@app.task(
    name="debug_task_1",
    bind=True,
    soft_time_limit=42,
    time_limit=300,
)
async def debug_task_1(self, *args, **kwargs):
    INC_LIST[0] += 1
    print(f'Hello there {INC_LIST[0]}')
    return INC_LIST[0]


@app.task(name="Debug task 2")
async def debug_task_2():
    print('Hello there 2')
    return "True"
