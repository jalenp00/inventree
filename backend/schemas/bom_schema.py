# schemas_bom_inventory.py
from __future__ import annotations
from decimal import Decimal
from typing import Annotated
from pydantic import BaseModel, Field

# match NUMERIC(18,6))
Qty = Annotated[Decimal, Field(ge=0, max_digits=18, decimal_places=6)]

# BOM LINE
class BOMLineIn(BaseModel):
    child_id: int
    quantity: Qty
    uom: str = "ea"

# BOM Line
class BOMLineOut(BaseModel):
    child_id: int
    quantity: Qty
    uom: str

# BOM with all lines
class BOMReplaceIn(BaseModel):
    parent_id: int
    lines: list[BOMLineIn]

# Bom with all lines
class BOMOut(BaseModel):
    child_id: int
    quantity: Qty
    uom: str

# Bulk payloads
class BOMReplaceBulkIn(BaseModel):
    boms: list[BOMReplaceIn]