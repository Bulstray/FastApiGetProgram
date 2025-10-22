from fastapi.security import HTTPBasic, HTTPBasicCredentials

from fastapi import Request, Depends, HTTPException, status
from typing import Annotated

from service.auth.redis_users_helper import redis_users
from templating.jinja_template import templates

from dependensies.programs import GetProgramsStorage

from typing import Any


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
        return None

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
