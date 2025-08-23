# app/routers/items.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from config.db import get_session
from models.item_model import Item
from schemas.item_schema import ItemIn, ItemOut
from services.inventory_service import InventoryService

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/", response_model=list[ItemOut])
async def list_items(db: AsyncSession = Depends(get_session)):

    res = await db.execute(select(Item).order_by(Item.id))
    return res.scalars().all()

@router.get("/{item_id}", response_model=ItemOut)
async def get_item(item_id: int, db: AsyncSession = Depends(get_session)):

    res = await db.execute(select(Item).where(Item.id == item_id))

    item = res.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=400, detail="Item not found.")
    
    item_out = ItemOut.model_validate(item)
    
    return item_out

@router.post("/", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
async def create_item(payload: ItemIn, db: AsyncSession = Depends(get_session)):

    exists = await db.execute(select(Item).where(Item.sku == payload.sku))

    if exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Item with that SKU already exists.")
    
    item = Item(**payload.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)

    service = InventoryService(db) # Maybe not the best spot?
    await service.check_and_create(item.id)

    return item

@router.patch("/{item_id}", response_model=ItemOut, status_code=status.HTTP_202_ACCEPTED)
async def update_item(item_id: int, payload: ItemIn, db: AsyncSession = Depends(get_session)):

    update_data = payload.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")
    
    res = await db.execute(update(Item).where(Item.id == item_id).values(**update_data).returning(Item))

    updated = res.fetchone()

    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    
    await db.commit()

    return ItemOut.model_validate(updated[0])


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_session)):
    res = await db.execute(select(Item).where(Item.id == item_id))
    item = res.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.delete(item)
    await db.commit()
    return {"details": "Item deleted successfully"}
