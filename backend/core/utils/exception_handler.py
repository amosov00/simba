from bson.errors import InvalidId
from fastapi import responses
from fastapi.exceptions import RequestValidationError, HTTPException
from pydantic import ValidationError
from starlette import status
from starlette.requests import Request

__all__ = ["exception_handlers"]


async def pydantic_exception_handler_func(request: Request, exc: ValidationError):
    resp = []
    for error in exc.errors():
        resp.append(
            {
                "field": error["loc"][-1],
                "message": error.get("msg"),
                "type": error.get("type"),
            }
        )
    return responses.UJSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=resp,
        headers={"Access-Control-Allow-Origin": "*"},
    )


async def http_exception_handler_func(request: Request, exception: HTTPException):
    if isinstance(exception.detail, list):
        content = [{"message": detail} for detail in exception.detail]
    elif isinstance(exception.detail, dict):
        content = exception.detail
    else:
        content = [{"message": exception.detail}]
    return responses.UJSONResponse(
        content=content,
        status_code=getattr(exception, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR),
        headers={"Access-Control-Allow-Origin": "*"},
    )


async def invalid_object_id_exception_handler(request: Request, exception: InvalidId):
    return responses.UJSONResponse(
        content=[{"message": "Invalid ID"}],
        status_code=status.HTTP_400_BAD_REQUEST,
        headers={"Access-Control-Allow-Origin": "*"},
    )


exception_handlers = {
    RequestValidationError: pydantic_exception_handler_func,
    HTTPException: http_exception_handler_func,
    status.HTTP_422_UNPROCESSABLE_ENTITY: pydantic_exception_handler_func,
    ValidationError: pydantic_exception_handler_func,
    InvalidId: invalid_object_id_exception_handler,
}
