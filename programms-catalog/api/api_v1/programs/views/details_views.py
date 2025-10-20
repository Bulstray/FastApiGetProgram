from fastapi import APIRouter, status

from dependensies.programs import ProgramByName, GetProgramsStorage
from schemas.programs.programs import ProgramRead

router = APIRouter()


@router.get(
    "/program/{name}/",
    response_model=ProgramRead,
)
def get_program_by_name(name: ProgramByName):
    return name


@router.delete(
    "/program/{name}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_program_by_name(name: ProgramByName):
    pass
