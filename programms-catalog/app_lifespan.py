from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from core.config import settings
from fastapi import FastAPI
from storage.program import ProgramsStorage


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:

    app.state.programs_storage = ProgramsStorage(
        hash_name=settings.redis.collection.program_hash,
    )

    yield
