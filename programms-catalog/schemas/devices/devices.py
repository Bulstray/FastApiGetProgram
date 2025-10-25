from pathlib import Path

from pydantic import BaseModel

from .devices_constant import DescriptionString, NameString, TypeDeviceString


class DeviceBase(BaseModel):
    type_device: TypeDeviceString
    name: NameString
    description: DescriptionString
    picture: str
    instruction: str


class DeviceRead(DeviceBase):
    """Модель для чтения данных"""


class Device(DeviceBase):
    """Модель для хранения данных о приоборе"""


class DeviceCreate(BaseModel):
    """Модель для добавления в базу данных"""

    type_device: TypeDeviceString
    name: NameString
    description: DescriptionString


class DevicePartialUpdate(BaseModel):
    """Модель для частичного обновления данных о приборе"""

    name: NameString | None = None
    description: DescriptionString | None = None
    picture: str | None = None
    instruction: str | None = None
