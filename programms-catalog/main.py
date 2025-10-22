import uvicorn
from api import router as api_router
from app_lifespan import lifespan
from fastapi import FastAPI
from rest import router as main_router

app = FastAPI(
    title="Programs",
    lifespan=lifespan,
)


app.include_router(main_router)
app.include_router(api_router)

if __name__ == "__main__":

    uvicorn.run(app)
