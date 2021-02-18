from fastapi import APIRouter, Query

from workers import agents

__all__ = ["router"]

router = APIRouter()


@router.post(
    "/",
    include_in_schema=False,
)
async def admin_backgroud_jobs(job_type: str = Query(..., alias="type")):
    job = {i: getattr(agents, i) for i in dir(agents) if "job" in i}.get(job_type)
    if job:
        await job.cast()
        return {"sucess": True}

    return {"sucess": False}
