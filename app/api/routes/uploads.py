from pydantic import BaseModel
from fastapi import APIRouter, File, Query, UploadFile

from app.services.storage import absolute_media_url, save_upload_file

router = APIRouter(prefix="/uploads", tags=["uploads"])


class UploadImageResponse(BaseModel):
    image_url: str
    relative_path: str


@router.post("/image", response_model=UploadImageResponse)
async def upload_image(
    file: UploadFile = File(...),
    folder: str = Query(default="general", min_length=1),
) -> UploadImageResponse:
    relative_path = await save_upload_file(file, folder)
    return UploadImageResponse(image_url=absolute_media_url(relative_path), relative_path=relative_path)
