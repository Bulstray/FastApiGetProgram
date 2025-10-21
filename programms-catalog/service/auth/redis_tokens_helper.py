from core.config import settings
from redis import Redis

from service.auth.tokens_helper import AbstractTokenHelper


class RedisTokensHelper(AbstractTokenHelper):
    def __init__(self, host: str, port: int, db: int, tokens_set_name: str) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )

        self.tokens_set_name = tokens_set_name

    def add_token(self, token: str) -> None:
        self.redis.sadd(
            self.tokens_set_name,
            token,
        )

    def token_exists(self, token: str) -> bool:
        return bool(self.redis.sismember(self.tokens_set_name, token))

    def delete_token(self, token: str) -> None:
        self.redis.srem(self.tokens_set_name, token)

    def get_tokens(self) -> set[str]:
        return self.redis.smembers(self.tokens_set_name)


redis_tokens = RedisTokensHelper(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.database.tokens,
    tokens_set_name=settings.redis.collection.tokens_set,
)
