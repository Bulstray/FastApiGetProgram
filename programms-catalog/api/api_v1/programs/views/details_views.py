from pathlib import Path

from dependensies.programs import GetProgramsStorage, ProgramByName
from fastapi import APIRouter, File, Form, UploadFile, status
from fastapi.responses import FileResponse
from schemas.programs.programs import ProgramUpdate

router = APIRouter()

UPLOADS_DIR = Path("uploads")


@router.get(
    "/program/{name}/",
)
def get_program_by_name(program: ProgramByName) -> FileResponse:
    return FileResponse(
        path=UPLOADS_DIR / f"{program.name}.zip",
        filename=f"{program.name}.zip",
    )


@router.put(
    "/{name}/",
)
def update_film(
    storage: GetProgramsStorage,
    program: ProgramByName,
    name_in: str | None = Form(None),
    description_in: str | None = Form(None),
    file_in: UploadFile | None = File(None),
):
    program_in = ProgramUpdate(name=name_in, description=description_in)
    storage.update(program=program, program_in=program_in, file_in=file_in)


@router.delete(
    "/program/{name}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_program_by_name(
    program: ProgramByName,
    storage: GetProgramsStorage,
) -> None:
    storage.delete_by_name_with_file(name=program.name)
