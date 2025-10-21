from fastapi import APIRouter

from .programs.views import router as program_router

router = APIRouter(prefix="/api_v1")

router.include_router(program_router)
