from core.config import settings
from redis import Redis

from .users_helper import AbstractUserHelper


class RedisUsersHelper(AbstractUserHelper):
    def __init__(self, host: str, port: int, db: int) -> None:
        self.redis = Redis(host=host, port=port, db=db, decode_responses=True)

    def get_user_password(self, username: str) -> str | None:
        return self.redis.get(name=username)


redis_users = RedisUsersHelper(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.database.users,
)
