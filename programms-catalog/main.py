from fastapi import FastAPI

from app_lifespan import lifespan


app = FastAPI(
    title="Programs",
    lifespan=lifespan,
)
