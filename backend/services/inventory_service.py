from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from config.db import get_session
from models.inventory_model import Inventory

class InventoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # Creates an inventory record if none exists
    async def check_and_create(self, item_id: int) -> Inventory:

         # check if already exists
        result = await self.db.execute(
            select(Inventory).where(Inventory.item_id == item_id)
        )
        inv = result.scalar_one_or_none()

        if inv:
            return inv

        # create new record
        inv = Inventory(item_id=item_id)
        self.db.add(inv)
        await self.db.commit()
        await self.db.refresh(inv)

        return inv