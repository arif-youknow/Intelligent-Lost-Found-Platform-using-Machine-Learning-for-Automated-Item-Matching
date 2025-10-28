from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class FoundItemBase(BaseModel):
    item_name: str
    found_date: datetime
    description: str

class FoundItemCreate(FoundItemBase):
    pass

class FoundItem(FoundItemBase):
    id: int
    item_image: Optional[str] = None
    item_status: str = Field("found", description="Status of the item: found or resolved")

    class Config:
        orm_mode = True