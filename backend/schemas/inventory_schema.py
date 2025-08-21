from __future__ import annotations
from decimal import Decimal
from typing import Annotated
from pydantic import Field
from enum import Enum
from type_defs.txn_type import TxnType
from config.schema import SchemaBase

# match NUMERIC(18,6))
Qty = Annotated[Decimal, Field(ge=0, max_digits=18, decimal_places=6)]

class AdjustType(str, Enum):
    adjustment_in = "adjustment_in"
    adjustment_out = "adjustment_out"

class InventoryOut(SchemaBase):
    item_id: int
    on_hand: Qty
    allocated: Qty
    incoming: Qty
    backordered: Qty # COMPUTED: allocated - on_hand (can be negative)
    available: Qty  # COMPUTED: on_hand - allocated (can be negative)
    available_to_build: Qty | None = None

class InventoryAdjustment(SchemaBase):
    item_id: int
    qty: Qty
    txn_type: TxnType
    reference: str | None = None

# Bulk adjustment
class InventorySetBulk(SchemaBase):
    items: list[InventoryAdjustment]