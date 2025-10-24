from fastapi import APIRouter

from .list_views import router as list_router

router = APIRouter(
    tags=["programs REST"],
    prefix="/devices",
    include_in_schema=False,
)


router.include_router(list_router)
