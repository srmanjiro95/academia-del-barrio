from pathlib import Path
from uuid import uuid4

import qrcode

from app.core.config import settings

QR_ROOT = Path("media/uploads/qr")
QR_ROOT.mkdir(parents=True, exist_ok=True)


def generate_member_qr() -> str:
    return uuid4().hex


def build_member_qr_image(qr_value: str) -> str:
    image = qrcode.make(qr_value)
    filename = f"{qr_value}.png"
    destination = QR_ROOT / filename
    image.save(destination)
    return f"/media/uploads/qr/{filename}"


def absolute_media_url(path: str) -> str:
    return f"{settings.public_base_url.rstrip('/')}{path}"
