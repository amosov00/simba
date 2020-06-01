from fastapi import FastAPI, exceptions, Request, responses
from pydantic import ValidationError
from starlette import status
from starlette.middleware import cors, authentication
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from api.routes import api_router
from core.utils import CustomJSONResponse, exception_handlers
from core.middleware import JWTAuthBackend
from database.init import mongo_client, mongo_db
from database.db_events import prepopulate_db, close_db_connection
from config import *

docs_config = {
    "docs_url": "/api/docs/",
    "redoc_url": "/api/redocs/",
    "openapi_url": "/api/docs/openapi.json",
} if not IS_PRODUCTION else {}

app = FastAPI(
    title="Elastoo",
    exception_handlers=exception_handlers,
    on_startup=[prepopulate_db],
    on_shutdown=[close_db_connection],
    **docs_config,
)

##########
# Database
##########

setattr(app, "mongo_client", mongo_client)
setattr(app, "mongo_db", mongo_db)

#########
# Routes
##########

app.include_router(api_router, prefix="/api", default_response_class=CustomJSONResponse)

##########
# Middlewares
##########

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(authentication.AuthenticationMiddleware, backend=JWTAuthBackend())

##########
# Misc
##########

SentryAsgiMiddleware(app)
