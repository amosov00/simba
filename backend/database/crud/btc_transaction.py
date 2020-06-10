from .base import BaseMongoCRUD


class BTCTransactionCRUD(BaseMongoCRUD):
    collection = "btc_transaction"
