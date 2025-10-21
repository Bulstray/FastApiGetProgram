import shutil
from collections.abc import Iterable
from pathlib import Path
from typing import cast

from core.config import settings
from fastapi import UploadFile
from pydantic import BaseModel
from redis import Redis
from schemas.programs.programs import Program, ProgramCreate

from .exceptions import ProgramAlreadyExistsError, UnsupportedFormatFileError

redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.database.programs,
    decode_responses=True,
)

UPLOAD_DIR = Path("uploads")


class ProgramsStorage(BaseModel):
    hash_name: str

    def __save_program(self, program: ProgramCreate, file: UploadFile) -> Program:

        file_path = UPLOAD_DIR / f"{program.name}.zip"

        with Path.open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        redis.hset(
            name=self.hash_name,
            key=program.name,
            value=program.model_dump_json(),
        )
        return Program(**program.model_dump())

    def __exists(self, name: str) -> bool:
        return cast(
            bool,
            redis.hexists(
                name=self.hash_name,
                key=name,
            ),
        )

    def create_or_raise_if_exists(
        self,
        program: ProgramCreate,
        file: UploadFile,
    ) -> None | Program:
        if self.__exists(name=program.name):
            raise ProgramAlreadyExistsError(program.name)

        if not cast(str, file.filename).endswith(".zip"):
            raise UnsupportedFormatFileError(file.filename)

        return self.__save_program(program=program, file=file)

    def get(self) -> list[Program]:
        return [
            Program.model_validate_json(json_data=json_data)
            for json_data in cast(
                Iterable[str],
                redis.hvals(
                    name=settings.redis.collection.program_hash,
                ),
            )
        ]

    def get_by_name(self, name: str) -> Program | None:
        if answer := redis.hget(name=self.hash_name, key=name):
            return Program.model_validate_json(cast(str, answer))

        return None


storage = ProgramsStorage(hash_name=settings.redis.collection.program_hash)
