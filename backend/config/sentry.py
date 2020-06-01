from os import getenv
from config.common import ENV, COMMIT

import sentry_sdk

SENTRY_DNS = getenv("SENTRY_DNS", "")

sentry_sdk.init(
    dsn=SENTRY_DNS,
    environment=ENV,
    release=COMMIT,
)
