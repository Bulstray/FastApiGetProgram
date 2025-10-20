from pathlib import Path

from pydantic import BaseModel, field_validator

from schemas.programs.exceptions import UnsupportedFormatFileError
from schemas.programs.programs_constants import DescriptionString, NameString


class ProgramBase(BaseModel):
    name: NameString
    description: DescriptionString

    file_path: Path

    @field_validator("file_path")
    def validate_file_path(self, v: Path) -> Path:
        archive_extensions: set[str] = {".zip", ".7z", ".rar"}

        if v.suffix.lower() not in archive_extensions:
            raise UnsupportedFormatFileError
        return v


class Program(ProgramBase):
    """Модель для хранения данных фильма"""


class ProgramCreate(ProgramBase):
    """Модель для создания программы"""


class ProgramUpdate(ProgramBase):
    """Модель для обновления информации"""
