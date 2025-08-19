from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from config.db import get_session
from models.inventory_txn_model import InventoryTransaction
from models.inventory_model import Inventory
from schemas.inventory_schema import InventoryOut, InventoryAdjustment
from schemas.inventory_txn import InventoryTxnOut

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.post("/adjust", response_model=InventoryOut)
async def adjust_inventory(payload:InventoryAdjustment, db: AsyncSession = Depends(get_session)):

    result = await db.execute(
        select(Inventory).where(Inventory.item_id == payload.item_id)
    )
    inv: Inventory | None = result.scalar_one_or_none()

    if not inv:
        inv = Inventory(item_id=payload.item_id)
        db.add(inv)
        await db.flush()
    
    txn = InventoryTransaction(**payload.model_dump())

    db.add(txn)
    await db.commit()
    await db.refresh(inv)

    return InventoryOut.model_validate(inv)

@router.get("/transactions/{item_id}", response_model=list[InventoryTxnOut])
async def get_all_txns(item_id:int, db: AsyncSession = Depends(get_session)):

    result = await db.execute(select(InventoryTransaction)
                              .where(InventoryTransaction.item_id == item_id)
                              .order_by(InventoryTransaction.created_at.desc()))
    
    txns = result.scalars().all()

    if not txns:
        raise HTTPException(status_code=404, detail="No Transactions found.")
    
    return [InventoryTxnOut.model_validate(txn) for txn in txns]

@router.get("/{item_id}", response_model=InventoryOut)
async def get_inventory(item_id: int, db: AsyncSession = Depends(get_session)):
    
    result = await db.execute(select(Inventory)
                              .where(Inventory.item_id == item_id))
    
    inv: Inventory | None = result.scalar_one_or_none()
    
    if not inv:
        raise HTTPException(status_code=404, detail="No inventory levels do not exist for this part.")
    
    return InventoryOut.model_validate(inv)
    