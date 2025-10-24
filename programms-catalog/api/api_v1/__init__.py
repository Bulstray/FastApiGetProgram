from fastapi import APIRouter, Depends, status

from .dependencies import api_token_required_for_unsafe_methods
from .devices.views import router as devices_router
from .programs.views import router as program_router

router = APIRouter(
    prefix="/api_v1",
    dependencies=[Depends(api_token_required_for_unsafe_methods)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe methods.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API token",
                    },
                },
            },
        },
    },
)

router.include_router(program_router)
router.include_router(devices_router)
