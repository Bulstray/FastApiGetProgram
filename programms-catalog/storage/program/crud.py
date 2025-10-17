from pydantic import BaseModel


class ProgramsStorage(BaseModel):
    hash_name: str
