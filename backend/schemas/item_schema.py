from pydantic import BaseModel
from typing import Literal
from decimal import Decimal
from config.schema import SchemaBase

class ItemIn(SchemaBase):
    sku: str
    uom: Literal["ea","lbs"]
    cost: Decimal
    type: Literal["product", "part", "raw"]
    description: str
    details: str

class ItemOut(SchemaBase):
    id: int
    sku: str
    uom: Literal["ea","lbs"]
    cost: Decimal
    type: Literal["product", "part", "raw"]
    description: str
    details: str
