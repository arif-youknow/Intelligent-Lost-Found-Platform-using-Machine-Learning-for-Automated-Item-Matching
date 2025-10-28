import datetime
from typing import Optional
from pydantic import BaseModel, Field


class LostItemBase(BaseModel):
    item_name: str
    lost_date: datetime
    description: str
class LostItemCreate(LostItemBase):
    pass

class LostItem(LostItemBase):
    id: int
    item_image: Optional[str] = None
    item_status: str = Field("lost", description="Status of the item: lost or resolved")

    class Config:
        orm_mode = True