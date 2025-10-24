from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from core.config import settings
from fastapi import FastAPI

from storage.devices.crud import DeviceStorage
from storage.program import ProgramsStorage


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:

    app.state.programs_storage = ProgramsStorage(
        hash_name=settings.redis.collection.program_hash,
    )
    app.state.devices_storage = DeviceStorage(
        hash_name=settings.redis.collection.device_hash,
    )

    yield
