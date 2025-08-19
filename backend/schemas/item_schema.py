from pydantic import BaseModel
from typing import Literal
from decimal import Decimal


class ItemIn(BaseModel):
    sku: str
    uom: Literal["ea","lbs"]
    cost: Decimal
    type: Literal["product", "part", "raw"]
    description: str
    details: str

class ItemOut(BaseModel):
    id: int
    sku: str
    uom: Literal["ea","lbs"]
    cost: Decimal
    type: Literal["product", "part", "raw"]
    description: str
    details: str


    class Config:
        from_attributes = True
