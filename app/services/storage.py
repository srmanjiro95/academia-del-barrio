from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

MEDIA_ROOT = Path("media/uploads")
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)


async def save_upload_file(upload: UploadFile, folder: str) -> str:
    target_dir = MEDIA_ROOT / folder
    target_dir.mkdir(parents=True, exist_ok=True)

    suffix = Path(upload.filename or "").suffix
    filename = f"{uuid4().hex}{suffix}"
    destination = target_dir / filename

    content = await upload.read()
    destination.write_bytes(content)

    return f"/media/uploads/{folder}/{filename}"
