# models_inventory.py
from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Integer, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property

from config.db import Base 


if TYPE_CHECKING:
    from .item_model import Item

class Inventory(Base):
    __tablename__ = "inventory"

    # PK + FK to items.id
    item_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("items.id", ondelete="CASCADE"),
        primary_key=True,
    )

    # Buckets (match NUMERIC(18,6) in Postgres)
    on_hand:     Mapped[Numeric] = mapped_column(Numeric(18, 6), nullable=False, server_default="0")
    allocated:   Mapped[Numeric] = mapped_column(Numeric(18, 6), nullable=False, server_default="0")
    incoming:    Mapped[Numeric] = mapped_column(Numeric(18, 6), nullable=False, server_default="0")
    backordered: Mapped[Numeric] = mapped_column(Numeric(18, 6), nullable=False, server_default="0")
    reorder_point: Mapped[Numeric] = mapped_column(Numeric(18, 6), nullable=True)
    reorder_point: Mapped[Numeric] = mapped_column(Numeric(18, 6), nullable=True)
    
    # Read-only computed field (compiled into SQL as (on_hand - allocated))
    available = column_property(on_hand - allocated)

    # 1–1 link back to Item
    item: Mapped["Item"] = relationship(
        "Item",
        back_populates="inventory",
        uselist=False,
        lazy="joined",
    )

    __table_args__ = (
        CheckConstraint("on_hand >= 0", name="inv_on_hand_nonneg"),
        CheckConstraint("allocated >= 0", name="inv_alloc_nonneg"),
        CheckConstraint("incoming >= 0", name="inv_incoming_nonneg"),
        CheckConstraint("backordered >= 0", name="inv_backorder_nonneg"),
    )

    def __repr__(self) -> str:
        return f"<Inventory item_id={self.item_id} on_hand={self.on_hand} allocated={self.allocated} available={self.available}>"
