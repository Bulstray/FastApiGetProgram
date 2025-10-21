import uvicorn
from api.api_v1.programs.views.list_views import router
from app_lifespan import lifespan
from fastapi import FastAPI

app = FastAPI(
    title="Programs",
    lifespan=lifespan,
)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app)
