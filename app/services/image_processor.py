"""
Image Processor - Handle image upload, background removal, and preprocessing
"""
from PIL import Image
from rembg import remove, new_session
from fastapi import UploadFile, HTTPException
import os
import uuid
from pathlib import Path
from typing import Optional

# Initialize rembg session (GPU if available)
try:
    rembg_session = new_session(providers=['CUDAExecutionProvider'])
except:
    rembg_session = new_session()

# Constants
UPLOAD_DIR = Path("static/uploads")
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
IMAGE_SIZE = (448, 448)

async def process_and_save_image(
    file: UploadFile,
    item_type: str,  # 'lost' or 'found'
    tracking_token: str
) -> str:
    """
    Process uploaded image:
    1. Validate file
    2. Remove background
    3. Resize to standard size
    4. Save to disk
    
    Returns:
        Relative path to saved image
    """
    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
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
        
        # Convert to RGB
        img = img.convert("RGB")
        
        # Resize before background removal (faster processing)
        img = img.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
        
        # Remove background
        img_no_bg = remove(img, session=rembg_session)
        
        # Convert back to RGB (rembg returns RGBA)
        img_final = img_no_bg.convert("RGB")
        
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
            print(f"⚠️ Image not found: {full_path}")
            return None
        
        img = Image.open(full_path).convert("RGB")
        
        # Ensure standard size
        if img.size != IMAGE_SIZE:
            img = img.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
        
        return img
    
    except Exception as e:
        print(f"⚠️ Failed to load image {image_path}: {e}")
        return None


import io  # Add this import at the top