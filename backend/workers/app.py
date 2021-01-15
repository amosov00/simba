import faust

from config import settings

__all__ = ["get_faust_app"]


def get_faust_app():
    broker_authentication = {}

    if settings.kafka.sasl_enable:
        broker_authentication["broker_credentials"] = faust.SASLCredentials(
            username=settings.kafka.sasl_username, password=settings.kafka.sasl_password
        )

    faust_app = faust.App(
        id=settings.kafka.app_name,
        broker=settings.kafka.server,
        broker_check_crcs=False,
        producer_max_request_size=4 * 1024 ** 3,
        consumer_max_fetch_size=2147483647,
        **broker_authentication,
    )

    return faust_app
