from fastapi import APIRouter

from .list_views import router as list_router

router = APIRouter(tags=["programs REST"], prefix="/programs")


router.include_router(list_router)
