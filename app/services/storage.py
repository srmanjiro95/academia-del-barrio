from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings

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


def absolute_media_url(path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return f"{settings.public_base_url.rstrip('/')}{path}"
