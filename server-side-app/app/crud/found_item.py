from sqlalchemy.orm import Session
from app.models.found_item import FoundItem as DBFoundItem
from app.schemas.found_item import FoundItemCreate


def create_found_item(db: Session, item_data: FoundItemCreate, image_path: str | None = None, item_status: str = 'found'):
    db_item = DBFoundItem(
        item_name=item_data.item_name,
        found_date=item_data.found_date,
        description=item_data.description,
        item_image=image_path,
        item_status=item_status.lower()
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

#get single item
def get_found_item(db: Session, item_id: int):
    return db.query(DBFoundItem).filter(DBFoundItem.id == item_id).first()
#get multiple item
def get_found_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBFoundItem).offset(skip).limit(limit).all()