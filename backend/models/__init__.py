# models/__init__.py
from config.db import Base
from .item_model import Item
from .inventory_model import Inventory
from .bom_model import Bom
from .inventory_txn_model import InventoryTransaction

# Attach relationships (only imports/wires them; no configure yet)
from .relationships import attach_relationships
attach_relationships()

# Configure mappers once relationships exist
from sqlalchemy.orm import configure_mappers
configure_mappers()

__all__ = ["Base", "Item", "Inventory", "InventoryTransaction", "Bom"]
