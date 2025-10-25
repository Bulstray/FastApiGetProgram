import os
import shutil
from collections.abc import Iterable
from pathlib import Path
from typing import cast

from core.config import settings
from pydantic import BaseModel
from fastapi import UploadFile
from redis import Redis
from schemas.devices.devices import Device, DeviceCreate

from .exceptions import DevicesAlreadyExistsError, UnsupportedFormatFileError

redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.database.devices,
    decode_responses=True,
)

BASEDIR = Path("uploads/device")


class DeviceStorage(BaseModel):

    hash_name: str

    def __load_program(self, file_path: Path, file: UploadFile) -> None:
        with Path.open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    def get(self) -> list[Device]:
        return [
            Device.model_validate_json(json_data=json_data)
            for json_data in cast(
                Iterable[str],
                redis.hvals(name=self.hash_name),
            )
        ]

    def __exist(self, name: str):
        return cast(
            bool,
            redis.hexists(
                name=self.hash_name,
                key=name,
            ),
        )

    def create(
        self,
        device: DeviceCreate,
        picture: UploadFile,
        instruction: UploadFile,
    ):

        path = BASEDIR / device.type_device / device.name
        os.makedirs(path, exist_ok=True)

        if not (
            picture.filename.endswith(".jpg") and instruction.filename.endswith(".pdf")
        ):
            raise UnsupportedFormatFileError

        path_picture = path / picture.filename
        path_instruction = path / instruction.filename

        self.__load_program(file_path=path_picture, file=picture)
        self.__load_program(file_path=path_instruction, file=instruction)

        device = Device(
            picture=picture.filename,
            instruction=picture.filename,
            **device.model_dump(),
        )

        redis.hset(
            name=self.hash_name,
            key=device.name,
            value=device.model_dump_json(),
        )

        return device

    def create_or_raise_if_exists(
        self,
        device_in: DeviceCreate,
        picture: UploadFile,
        instruction: UploadFile,
    ) -> Device | None:
        if not self.__exist(name=device_in.name):
            return self.create(
                device=device_in,
                picture=picture,
                instruction=instruction,
            )

        raise DevicesAlreadyExistsError(device_in)

    def get_by_name(self, name: str) -> Device | None:
        if answer := redis.hget(name=self.hash_name, key=name):
            return Device.model_validate_json(cast(str, answer))

        return None

    def delete_by_name(self, name: str) -> None:
        redis.hdel(settings.redis.collection.device_hash, name)


storage = DeviceStorage(
    hash_name=settings.redis.collection.device_hash,
)
