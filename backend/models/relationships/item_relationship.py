from models.item_model import Item
from models.bom_model import Bom
from sqlalchemy.orm import relationship

Item.bom_children = relationship(
    Bom,
    back_populates="parent",
    foreign_keys=[Bom.parent_id],
    cascade="all, delete-orphan"
)

Item.bom_parents = relationship(
    Bom,
    back_populates="child",
    foreign_keys=[Bom.child_id]
)