from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from config.db import get_session
from models.bom_model import Bom
from schemas.bom_schema import BomLineIn, BomLineOut

router = APIRouter(prefix="/boms", tags=["boms"])

# Create Bom
@router.post("/{item_id}", response_model=BomLineOut, status_code=status.HTTP_201_CREATED)
async def create_bomline(item_id: int, payload: BomLineIn, db: AsyncSession = Depends(get_session)):
    bom_exists = await db.execute(select(Bom).where(Bom.child_id == payload.child_id))
    if bom_exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Bom with that id already exists.")
    bom = Bom(**payload.model_dump())
    bom.parent_id = item_id
    db.add(bom)
    await db.commit()
    await db.refresh(bom)
    return bom

# Get Child BOMs
@router.get("/child/{item_id}", response_model=list[BomLineOut])
async def list_child_boms(item_id: int, db: AsyncSession = Depends(get_session)):
    res = await db.execute(select(Bom).where(Bom.parent_id == item_id).order_by(Bom.child_id))
    return res.scalars().all()

# Get Parent BOMs
@router.get("/parent/{item_id}", response_model=list[BomLineOut])
async def list_parent_boms(item_id: int, db: AsyncSession = Depends(get_session)):
    res = await db.execute(select(Bom).where(Bom.child_id == item_id).order_by(Bom.parent_id))
    return res.scalars().all()

# Edit Bom
@router.patch("/{item_id}", response_model=BomLineOut)
async def update_bom(item_id: int, payload: BomLineIn, db: AsyncSession = Depends(get_session)):

    update_data = payload.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")
    
    res = await db.execute(update(Bom).where((Bom.parent_id == item_id) & (Bom.child_id == payload.child_id)).values(**update_data).returning(Bom))

    updated = res.fetchone()

    if not updated:
        raise HTTPException(status_code=404, detail="BOM line not found")
    
    await db.commit()

    return BomLineOut.model_validate(updated[0])

# Delete Bom
@router.delete("/{item_id}", response_model=BomLineOut)
async def delete_bom(item_id: int, payload: BomLineIn, db: AsyncSession = Depends(get_session)):

    res = await db.execute(delete(Bom).where((Bom.parent_id == item_id) & (Bom.child_id == payload.child_id)))

    if res.rowcount == 0:
        raise HTTPException(status_code=404, detail="Bom line not found.")
    
    await db.commit()

    return {"detail": "Bom line deleted successfully"}
