from collections.abc import Generator

import pytest
from main import app
from service.auth.redis_tokens_helper import redis_tokens
from starlette.testclient import TestClient


@pytest.fixture
def client() -> Generator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_token() -> Generator[str]:
    token = redis_tokens.generate_and_save_token()
    yield token
    redis_tokens.delete_token(token)


@pytest.fixture
def auth_client(
    auth_token: str,
) -> Generator[TestClient]:
    headers = {"Authorization": f"Bearer {auth_token}"}
    with TestClient(app, headers=headers) as client:
        yield client
