import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.db import Base, engine
import app.models  # noqa: F401
from app.services.realtime import start_listener


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    stop_event = asyncio.Event()
    listener_task = asyncio.create_task(start_listener(stop_event))
    yield
    stop_event.set()
    await listener_task


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(api_router)
