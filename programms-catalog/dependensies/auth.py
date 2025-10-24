from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from service.auth.redis_users_helper import redis_users

from dependensies.programs import GetProgramsStorage

user_basic_auth = HTTPBasic(
    scheme_name="Basic Auth",
    description="Basic username + password auth",
    auto_error=True,
)


def validate_basic_auth(
    request: Request,
    storage: GetProgramsStorage,
    credentials: Annotated[HTTPBasicCredentials, Depends(user_basic_auth)],
):
    if credentials and redis_users.validate_user_password(
        username=credentials.username,
        password=credentials.password,
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
