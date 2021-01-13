from datetime import timedelta

from .common import IS_PRODUCTION

ALGORITHM = "HS256"

if IS_PRODUCTION:
    EXPIRES_DELTA = timedelta(minutes=5)
else:
    EXPIRES_DELTA = timedelta(days=1)
