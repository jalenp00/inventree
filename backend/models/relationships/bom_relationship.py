from models.item_model import Item
from models.bom_model import Bom
from sqlalchemy.orm import relationship

Bom.parent = relationship(
    Item,
    back_populates="bom_children",
    foreign_keys=[Bom.parent_id]
)

Bom.child = relationship(
    Item,
    back_populates="bom_parents",
    foreign_keys=[Bom.child_id]
)