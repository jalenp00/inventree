# models/inventory_txn_model.py
from __future__ import annotations
from sqlalchemy import (
    BigInteger, Integer, Numeric, Text, DateTime, CheckConstraint,
    ForeignKey, Enum, Index
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from config.db import Base
from type_defs.txn_type import TxnType


class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    item_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("items.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    qty: Mapped[Numeric] = mapped_column(
        Numeric(18, 6),
        nullable=False,
    )

    txn_type: Mapped[TxnType] = mapped_column(
        Enum(TxnType, name="inventory_txn_type", native_enum=True),
        nullable=False,
    )

    reference: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    on_hand: Mapped[Numeric] = mapped_column(
        Numeric(18, 6), nullable=False, server_default="0"
    )

    __table_args__ = (
        CheckConstraint("qty > 0", name="inv_txn_qty_pos"),
        Index("idx_inv_txn_type", "txn_type"),
        Index("idx_inv_txn_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<InvTxn id={self.id} item_id={self.item_id} type={self.txn_type} qty={self.qty}>"
