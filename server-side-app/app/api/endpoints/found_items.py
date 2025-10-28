from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pathlib import Path
import datetime
from starlette.concurrency import run_in_threadpool 
from app.core.database import get_db
from app.crud import found_item as crud_found_item
from app.schemas.found_item import FoundItem as FoundItemSchema, FoundItemCreate

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

router = APIRouter(
    prefix="/found-items",
    tags=["found-items"]
)

@router.post("/", response_model=FoundItemSchema)
async def create_found_item_endpoint(
    item_name: str = Form(...),
    found_date: str = Form(...),
    description: str = Form(...),
    item_image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_path = None
    if item_image and item_image.filename:
        file_extension = Path(item_image.filename).suffix
        unique_filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}{file_extension}"
        file_location = UPLOAD_DIR / unique_filename
        file_contents = await item_image.read()
        
        try:
           
            await run_in_threadpool(file_location.write_bytes, file_contents)
            
            image_path = f"/uploads/{unique_filename}"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"ফাইল আপলোড করতে সমস্যা হয়েছে: {e}")

    try:
        parsed_found_date = datetime.datetime.strptime(found_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="তারিখের ফরম্যাট ভুল। YYYY-MM-DD ফরম্যাট আশা করা হচ্ছে।")

    item_create_data = FoundItemCreate(
        item_name=item_name,
        found_date=parsed_found_date,
        description=description
    )

    db_item = crud_found_item.create_found_item(
        db=db,
        item_data=item_create_data,
        image_path=image_path,
        item_status='found'
    )
    return db_item

@router.get("/", response_model=list[FoundItemSchema])
def read_found_items_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud_found_item.get_found_items(db, skip=skip, limit=limit)
    return items