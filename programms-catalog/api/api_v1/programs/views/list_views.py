from typing import Annotated

from fastapi import APIRouter, Form, UploadFile, status
from schemas.programs.programs import Program, ProgramCreate, ProgramRead
from storage.program.crud import storage

router = APIRouter(prefix="/programs", tags=["Programs"])


@router.get("/", response_model=list[ProgramRead])
def read_program_list() -> list[Program]:
    return storage.get()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Program)
def add_program(
    file: UploadFile,
    name: Annotated[str, Form(...)],
    description: Annotated[str, Form(...)],
) -> None:
    program_create = ProgramCreate(
        name=name,
        description=description,
    )

    storage.create_or_raise_if_exists(
        program=program_create,
        file=file,
    )
