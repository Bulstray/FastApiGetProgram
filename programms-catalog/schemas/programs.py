from pathlib import Path
from typing import Annotated

from annotated_types import Len, MaxLen
from pydantic import BaseModel, field_validator

NAME_MIN_LENGTH = 3
NAME_MAX_LENGTH = 50

NameString = Annotated[
    str,
    Len(
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_MAX_LENGTH,
    ),
]


DESCRIPTION_MAX_LENGTH = 200

DescriptionString = Annotated[str, MaxLen(DESCRIPTION_MAX_LENGTH)]


class ProgramBase(BaseModel):
    name: NameString
    description: DescriptionString

    file_path: Path

    @field_validator("file_path")
    def validate_file_path(cls, v: Path) -> Path:
        archive_extensions: set[str] = {".zip", ".7z", ".rar"}

        if v.suffix.lower() not in archive_extensions:
            raise ValueError(
                f"Неподдерживаемый формат архива: {v.suffix}. "
                f"Поддерживаемые форматы: {', '.join(archive_extensions)}",
            )
        return v


class Program(ProgramBase):
    """Модель для хранения данных фильма"""


class ProgramCreate(ProgramBase):
    """Модель для создания программы"""


class ProgramUpdate(ProgramBase):
    """Модель для обновления информации"""
