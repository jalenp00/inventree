# schemas_bom_inventory.py
from __future__ import annotations
from decimal import Decimal
from typing import Annotated
from pydantic import Field
from config.schema import SchemaBase

# match NUMERIC(18,6))
Qty = Annotated[Decimal, Field(ge=0, max_digits=18, decimal_places=6)]

# BOM LINE
class BOMLineIn(SchemaBase):
    child_id: int
    quantity: Qty
    uom: str = "ea"

# BOM Line
class BOMLineOut(SchemaBase):
    child_id: int
    quantity: Qty
    uom: str

# BOM with all lines
class BOMReplaceIn(SchemaBase):
    parent_id: int
    lines: list[BOMLineIn]

# Bom with all lines
class BOMOut(SchemaBase):
    child_id: int
    quantity: Qty
    uom: str

# Bulk payloads
class BOMReplaceBulkIn(SchemaBase):
    boms: list[BOMReplaceIn]