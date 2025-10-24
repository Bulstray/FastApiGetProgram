from fastapi import APIRouter

from .list_views import router as list_router
from .detail_views import router as detail_router

router = APIRouter(
    prefix="/devices",
    tags=["Device"],
)

router.include_router(list_router)
router.include_router(detail_router)
