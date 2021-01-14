from .base import BaseMongoCRUD

__all__ = ["UserAddressesArchiveCRUD"]


class UserAddressesArchiveCRUD(BaseMongoCRUD):
    collection = "user_addresses_archive"
