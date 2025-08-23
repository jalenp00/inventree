from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from config.db import get_session
from models.inventory_txn_model import InventoryTransaction
from models.inventory_model import Inventory
from schemas.inventory_schema import InventoryOut, InventoryAdjustment
from schemas.inventory_txn import InventoryTxnOut
from queries.inventory_q import InventoryQ
from services.inventory_service import InventoryService
from models.item_model import Item

router = APIRouter(prefix="/inventory", tags=["inventory"])

'''
Gets all rows from inventory table
Gets available_to_build from query
Gets sku from Items table
'''
@router.get("/", response_model=list[InventoryOut])
async def get_all_inventory(db: AsyncSession = Depends(get_session)):
    res = await db.execute(
        select(Inventory).options(selectinload(Inventory.item))
    )

    inv = res.scalars().all()
    full_inventory = []

    for item in inv:
        avail_result = await db.execute(InventoryQ.get_available_to_build, {"item_id": item.item.id})
        sku = await db.execute(select(Item.sku).where(Item.id == item.item.id))
        item.sku = sku.scalar_one()
        inv_out = InventoryOut.model_validate(item)
        inv_out.available_to_build = avail_result.scalar_one_or_none()
        full_inventory.append(inv_out)
    return full_inventory

@router.get("/transactions/{item_id}", response_model=list[InventoryTxnOut])
async def get_all_txns(item_id: int, db: AsyncSession = Depends(get_session)):

    res = await db.execute(select(InventoryTransaction)
                              .where(InventoryTransaction.item_id == item_id)
                              .order_by(InventoryTransaction.created_at.desc()))
    
    txns = res.scalars().all()

    if not txns:
        raise HTTPException(status_code=404, detail="No Transactions found.")
    
    return [InventoryTxnOut.model_validate(txn) for txn in txns]

@router.get("/{item_id}", response_model=InventoryOut)
async def get_inventory(item_id: int, db: AsyncSession = Depends(get_session)):
    
    res = await db.execute(select(Inventory)
                              .where(Inventory.item_id == item_id))
    
    inv: Inventory | None = res.scalar_one_or_none()
    
    if not inv:
        raise HTTPException(status_code=404, detail="No inventory levels do not exist for this part.")
    
    avail_result = await db.execute(InventoryQ.get_available_to_build, {"item_id": item_id})
    available = avail_result.scalar()

    inv_out = InventoryOut.model_validate(inv)
    inv_out.available_to_build = available
    
    return inv_out

@router.post("/adjust", response_model=InventoryOut)
async def adjust_inventory(payload: InventoryAdjustment, db: AsyncSession = Depends(get_session)):

    service = InventoryService(db) # Maybe not the best spot?
    
    inv = await service.check_and_create(payload.item_id)
    
    data = payload.model_dump()
    data["on_hand"] = inv.on_hand + payload.qty

    txn = InventoryTransaction(**data)

    db.add(txn)
    await db.commit()
    await db.refresh(inv)

    return InventoryOut.model_validate(inv)
    