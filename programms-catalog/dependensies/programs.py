from typing import Annotated, cast

from fastapi import Depends, HTTPException, Request, status
from schemas.programs.programs import Program
from storage.program.crud import ProgramsStorage


def get_programs_storage(request: Request) -> ProgramsStorage:
    return cast(ProgramsStorage, request.app.state.programs_storage)


GetProgramsStorage = Annotated[
    ProgramsStorage,
    Depends(get_programs_storage),
]


def prefetch_program_by_name(
    name: str,
    storage: GetProgramsStorage,
) -> Program:
    program: Program | None = storage.get_by_name(name=name)

    if program:
        return program

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Program not found",
    )


ProgramByName = Annotated[Program, Depends(prefetch_program_by_name)]
