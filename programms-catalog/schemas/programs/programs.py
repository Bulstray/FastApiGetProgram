from pydantic import BaseModel

from schemas.programs.programs_constants import DescriptionString, NameString


class ProgramBase(BaseModel):
    name: NameString
    description: DescriptionString


class ProgramRead(ProgramBase):
    """Модель для просмотра программ"""


class Program(ProgramBase):
    """Модель для хранения данных программ"""


class ProgramCreate(ProgramBase):
    """Модель для создания программы"""


class ProgramUpdate(ProgramBase):
    """Модель для обновления информации"""
