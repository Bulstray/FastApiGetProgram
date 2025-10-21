from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from service.auth.redis_tokens_helper import redis_tokens

UNSAFE_METHODS = frozenset({"POST", "PUT", "DELETE"})


static_api_token = HTTPBearer(
    auto_error=False,
    scheme_name="Static API token",
    description="Your Static API token from developer portal",
)


def validate_api_token(api_token: HTTPAuthorizationCredentials) -> None:
    if redis_tokens.token_exists(
        token=api_token.credentials,
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API token",
    )


def api_token_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[HTTPAuthorizationCredentials, Depends(static_api_token)],
) -> None:
    if request.method not in UNSAFE_METHODS:
        return None

    if api_token:
        return validate_api_token(api_token=api_token)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API token required",
    )
