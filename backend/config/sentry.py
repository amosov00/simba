from os import getenv
from config.common import ENV, COMMIT

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

SENTRY_DSN = getenv("SENTRY_DSN", "")

sentry_sdk.init(
    dsn=SENTRY_DSN, release=COMMIT, environment=ENV, attach_stacktrace=True, integrations=[CeleryIntegration()]
)
