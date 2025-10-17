from app_lifespan import lifespan
from fastapi import FastAPI

app = FastAPI(
    title="Programs",
    lifespan=lifespan,
)
