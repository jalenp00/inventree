from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Integer, Numeric, ForeignKey, Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.db import Base

if TYPE_CHECKING:
    from .item_model import Item

class Bom(Base):
    __tablename__ = "bom"

    parent_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("items.id", ondelete="CASCADE"), primary_key=True
    )
    child_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("items.id", ondelete="RESTRICT"), primary_key=True
    )
    quantity:   Mapped[float] = mapped_column(Numeric(18,6), nullable=False)
    uom:       Mapped[str]   = mapped_column(Text, nullable=False, default="ea")

    parent = relationship("Item", foreign_keys=[parent_id], back_populates="bom_children")
    child  = relationship("Item", foreign_keys=[child_id],  back_populates="bom_parent")

    __table_args__ = (
        CheckConstraint("qty_per > 0", name="bom_qty_pos"),
        CheckConstraint("scrap_pct >= 0", name="bom_scrap_nonneg"),
        CheckConstraint("parent_id <> child_id", name="bom_no_self_ref"),
    )
