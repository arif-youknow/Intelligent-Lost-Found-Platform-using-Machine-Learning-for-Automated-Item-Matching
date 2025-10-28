import datetime
from fastapi import APIRouter, Depends, File, Form, HTTPException,UploadFile
from pathlib import Path
from fastapi.concurrency import run_in_threadpool
from app.core.database import get_db
from app.crud import lost_item as crud_lost_item
from app.schemas.lost_item import LostItem as LostItemScema, LostItemCreate
from sqlalchemy.orm import Session


UPLOAD_DIR_LOST = Path("uploads/lost")
UPLOAD_DIR_LOST.mkdir(exist_ok=True , parents=True)

router = APIRouter(
    prefix="/lost-items",
    tags=["lost-items"]
)

@router.post("/", response_model=LostItemScema)
async def create_found_item_endpoint(
    item_name: str = Form(...),
    lost_date: str = Form(...),
    description: str = Form(...),
    item_image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_path = None
    if item_image and item_image.filename:
        file_extension = Path(item_image.filename).suffix
        unique_filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}{file_extension}"
        file_location = UPLOAD_DIR_LOST / unique_filename
        file_contents = await item_image.read()
        try:
           await run_in_threadpool(file_location.write_bytes, file_contents)   
           image_path = f"/uploads/lost{unique_filename}"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Problem uploading file: {e}")
        try:
            parsed_lost_date = datetime.datetime.strptime(lost_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Incorrect date format. YYYY-MM-DD format is expected.")

    item_create_data = LostItemCreate(
        item_name=item_name,
        lost_date=parsed_lost_date,
        description=description
    )
    db_item = crud_lost_item.create_lost_item(
        db=db,
        item_data=item_create_data,
        image_path=image_path,
        item_status='lost'
    )
    return db_item

@router.get("/", response_model=list[LostItemScema])
def read_lost_items_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud_lost_item.get_lost_items(db, skip=skip, limit=limit)
    return items
        
    