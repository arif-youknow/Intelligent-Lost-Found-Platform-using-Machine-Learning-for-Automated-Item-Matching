from sqlalchemy.orm import Session
from app.models.lost_item import LostItem as DBLostItem
from app.schemas.lost_item import LostItemCreate


def create_lost_item(db:Session,item_data: LostItemCreate, image_path: str | None = None, item_status: str = 'lost' ):
    db_item = DBLostItem(
        item_name=item_data.item_name,
        found_date=item_data.lost_date,
        description=item_data.description,
        item_image=image_path,
        item_status=item_status.lower()
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

#get single item
def get_lost_item(db: Session, item_id: int):
    return db.query(DBLostItem).filter(DBLostItem.id == item_id).first()
#get multiple item
def get_lost_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBLostItem).offset(skip).limit(limit).all()