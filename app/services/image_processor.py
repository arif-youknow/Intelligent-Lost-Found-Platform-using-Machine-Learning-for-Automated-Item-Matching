"""
Image Processor - Handle image upload, background removal, and preprocessing
"""
from PIL import Image
from app.config import settings
from rembg import remove, new_session
from fastapi import UploadFile, HTTPException
import os
import uuid
from pathlib import Path
from typing import Optional, cast
import io  

# Initialize rembg session (GPU if available)
try:
    rembg_session = new_session(providers=['CUDAExecutionProvider'])
except:
    rembg_session = new_session()



# Constants
upload_path_str = cast(str, settings.UPLOAD_DIR)
UPLOAD_DIR = Path(upload_path_str)
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
IMAGE_SIZE = (448, 448)





async def process_and_save_image(
    file: UploadFile,
    item_type: str, 
    tracking_token: str
) -> str:
    
    # Validate file extension
    safe_filename = file.filename if file.filename else "unknown.jpg"
    file_ext = Path(safe_filename).suffix.lower()
    
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {ALLOWED_EXTENSIONS}"
        )
    
    # Read file
    contents = await file.read()
    
    # Check file size
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {MAX_FILE_SIZE_MB}MB"
        )
    
    
    
    try:
        # Open image
        img = Image.open(io.BytesIO(contents))
        
        
        # Remove background
        img_no_bg_raw = remove(img, session=rembg_session)
           
        
        if not isinstance(img_no_bg_raw, Image.Image):
            
            img_no_bg = Image.open(io.BytesIO(img_no_bg_raw)).convert("RGBA")
        else:
            img_no_bg = img_no_bg_raw
            
        
        img_final = Image.new("RGB", img_no_bg.size, (255, 255, 255))
        
        if img_no_bg.mode == 'RGBA':
            img_final.paste(img_no_bg, mask=img_no_bg.split()[3])
        else:
            img_final.paste(img_no_bg)
        
        # Resize
        img_final = img_final.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
        
        
        # Generate filename
        filename = f"{tracking_token}_{uuid.uuid4().hex[:8]}{file_ext}"
        
        # Create directory if not exists
        save_dir = UPLOAD_DIR / item_type
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Save path
        file_path = save_dir / filename
        
        # Save image
        img_final.save(file_path, quality=95, optimize=True)
        
        # Return relative path
        return f"uploads/{item_type}/{filename}"
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Image processing failed: {str(e)}"
        )


def load_clean_image(image_path: str) -> Optional[Image.Image]:
    """
    Load a preprocessed image from disk
    
    Args:
        image_path: Relative path to image
    
    Returns:
        PIL Image or None if failed
    """
    try:
        full_path = Path("static") / image_path
        
        if not full_path.exists():
            print(f"Image not found: {full_path}")
            return None
        
        img = Image.open(full_path).convert("RGB")
        
        # Ensure standard size
        if img.size != IMAGE_SIZE:
            img = img.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
        
        return img
    
    except Exception as e:
        print(f"Failed to load image {image_path}: {e}")
        return None


