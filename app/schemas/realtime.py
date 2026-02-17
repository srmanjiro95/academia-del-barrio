from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class RealtimeEvent(BaseModel):
    topic: str
    payload: dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)
