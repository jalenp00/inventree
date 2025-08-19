from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from config.db import get_session
from models.bom_model import Bom
from schemas.bom_schema import BOMLineIn, BOMLineOut, BOMOut

router = APIRouter(prefix="/boms", tags=["boms"])

@router.post("/{item_id}", response_model=BOMLineOut, status_code=status.HTTP_201_CREATED)
async def create_bomline(item_id: int, payload:BOMLineIn, db: AsyncSession = Depends(get_session)):
    bom_exists = await db.execute(select(Bom).where(Bom.child_id == payload.child_id))
    if bom_exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Bom with that id already exists.")
    bom = Bom(**payload.model_dump())
    bom.parent_id = item_id
    db.add(bom)
    await db.commit()
    await db.refresh(bom)
    return bom

@router.get("/{item_id}", response_model=list[BOMOut])
async def list_boms(item_id: int, db: AsyncSession = Depends(get_session)):
    res = await db.execute(select(Bom).where(Bom.parent_id==item_id).order_by(Bom.child_id))
    return res.scalars().all()