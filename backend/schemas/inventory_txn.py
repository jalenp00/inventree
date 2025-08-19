# schemas/inventory_txn.py
from config.schema import SchemaBase
from datetime import datetime
from models.inventory_txn_model import TxnType

class InventoryTxnOut(SchemaBase):
    id: int
    item_id: int
    qty: float
    txn_type: TxnType
    reference: str | None
    created_at: datetime
    on_hand: float
