from pydantic import BaseModel
from pydantic_settings import BaseSettings


class RedisDatabaseConfig(BaseModel):
    default: int = 0
    tokens: int = 0
    users: int = 2
    programs: int = 3


class RedisConnectionConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379


class RedisCollectionConfig(BaseModel):
    tokens_set: str = "tokens"
    program_hash: str = "program"


class RedisConfig(BaseModel):
    connection: RedisConnectionConfig = RedisConnectionConfig()
    database: RedisDatabaseConfig = RedisDatabaseConfig()
    collection: RedisCollectionConfig = RedisCollectionConfig()


class Settings(BaseSettings):
    redis: RedisConfig = RedisConfig()


settings = Settings()
