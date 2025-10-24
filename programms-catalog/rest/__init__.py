from fastapi import APIRouter

from rest.main_views import router as main_router
from rest.programs import router as list_views_program_router
from rest.device import router as list_views_device_router

router = APIRouter()

router.include_router(main_router)
router.include_router(list_views_program_router)
router.include_router(list_views_device_router)
