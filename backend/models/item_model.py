from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, Numeric, TEXT, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.db import Base

if TYPE_CHECKING:
    from .inventory_model import Inventory

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sku: Mapped[str] = mapped_column(String(15), unique=True, index=True)
    uom: Mapped[str] = mapped_column(String(10), nullable=False)
    cost: Mapped[Numeric] = mapped_column(Numeric(12, 6), nullable=True)
    type: Mapped[str] = mapped_column(TEXT, nullable=False)
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    details: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    __table_args__ = (CheckConstraint("type IN ('product','part','raw')", name="item_type_ck"),)


    # item.inventory
    inventory: Mapped["Inventory"] = relationship(
        "Inventory",
        back_populates="item",
        uselist=False,
        cascade="all, delete-orphan",
    )

