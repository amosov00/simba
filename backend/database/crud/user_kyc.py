from .base import BaseMongoCRUD

__all__ = ["UserKYCCRUD"]


class UserKYCCRUD(BaseMongoCRUD):
    collection = "user_kyc"
