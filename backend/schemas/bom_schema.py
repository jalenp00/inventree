# schemas_bom_inventory.py
from __future__ import annotations
from decimal import Decimal
from typing import Annotated
from pydantic import Field
from config.schema import SchemaBase

# match NUMERIC(18,6))
Qty = Annotated[Decimal, Field(ge=0, max_digits=18, decimal_places=6)]

# BOM LINE
class BomLineBase(SchemaBase):
    child_id: int
    qty: Qty
    uom: str = "ea"

class BomLineIn(BomLineBase):
    pass

class BomLineOut(BomLineBase):
    parent_id: int
    