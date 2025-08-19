# relationships/inventory_txn_relationship.py
from __future__ import annotations

from sqlalchemy.orm import relationship

from models.item_model import Item
from models.inventory_txn_model import InventoryTransaction

# Item → InventoryTransaction (one-to-many)
# Keep newest first for convenience when you load the collection
Item.inventory_txns = relationship(
    InventoryTransaction,
    back_populates="item",
    cascade="all, delete-orphan",
    passive_deletes=True,
    lazy="selectin",
    order_by=InventoryTransaction.created_at.desc(),
)

# InventoryTransaction → Item (many-to-one)
InventoryTransaction.item = relationship(
    Item,
    back_populates="inventory_txns",
    lazy="joined",
)
