from __future__ import annotations
from decimal import Decimal
from typing import Annotated
from pydantic import BaseModel, Field

# match NUMERIC(18,6))
Qty = Annotated[Decimal, Field(ge=0, max_digits=18, decimal_places=6)]

class InventoryOut(BaseModel):
    item_id: int
    on_hand: Qty
    allocated: Qty
    incoming: Qty
    backordered: Qty
    available: Qty  # on_hand - allocated (can be negative)

class InventorySet(BaseModel):
    item_id: int
    on_hand: Qty = Decimal("0")
    allocated: Qty = Decimal("0")
    incoming: Qty = Decimal("0")
    backordered: Qty = Decimal("0")

class InventoryDelta(BaseModel):
    item_id: int
    on_hand: Qty = Decimal("0")
    allocated: Qty = Decimal("0")
    incoming: Qty = Decimal("0")
    backordered: Qty = Decimal("0")

# Bulk payloads
class InventorySetBulk(BaseModel):
    items: list[InventorySet]

class InventoryDeltaBulk(BaseModel):
    items: list[InventoryDelta]