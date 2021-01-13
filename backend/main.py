from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware import cors, authentication

from api.routes import api_router
from config import *
from core.middleware import JWTAuthBackend
from core.utils import CustomJSONResponse, exception_handlers
from database.db_events import test_db_connection, prepopulate_db, close_db_connection
from database.init import mongo

docs_config = (
    {
        "redoc_url": "/api/docs/",
        "openapi_url": "/api/docs/openapi.json",
    }
    if not IS_PRODUCTION
    else {}
)

app = FastAPI(
    title="Simba",
    exception_handlers=exception_handlers,
    on_startup=[test_db_connection, prepopulate_db],
    on_shutdown=[close_db_connection],
    **docs_config,
)

##########
# Database
##########

setattr(app, "mongo", mongo)

#########
# Routes
##########

app.include_router(api_router, prefix="/api", default_response_class=CustomJSONResponse)

##########
# Middlewares
##########

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(authentication.AuthenticationMiddleware, backend=JWTAuthBackend())

##########
# Misc
##########

SentryAsgiMiddleware(app)
