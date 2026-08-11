import os
import shutil
import uuid
 
IMAGES_DIR = "images"

def ensure_images_dir():
    os.makedirs(IMAGES_DIR, exist_ok=True)

def save_card_image(source_path: str) -> str:
    if not os.path.isfile(source_path):
        raise FileNotFoundError(f"No file found at {source_path}")
 
    ext = os.path.splitext(source_path)[1].lower()
    allowed_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
    if ext not in allowed_extensions:
        raise ValueError(
            f"Unsupported image type '{ext}'. Allowed: {', '.join(sorted(allowed_extensions))}"
        )
 
    ensure_images_dir()

    new_filename = f"{uuid.uuid4().hex}{ext}"
    destination_path = os.path.join(IMAGES_DIR, new_filename)
 
    shutil.copy2(source_path, destination_path)
 
    return destination_path 