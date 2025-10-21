__all__ = ("router",)

from fastapi import APIRouter, Depends, status

from api.api_v1.programs.dependencies import api_token_required_for_unsafe_methods

from .details_views import router as details_router
from .list_views import router as list_router

router = APIRouter(
    prefix="/programs",
    tags=["Programs"],
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


router.include_router(list_router)
router.include_router(details_router)
