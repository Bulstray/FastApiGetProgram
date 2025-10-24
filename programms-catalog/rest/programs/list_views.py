from pathlib import Path
from typing import Any

from dependensies.auth import validate_basic_auth
from dependensies.programs import GetProgramsStorage, ProgramByName
from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse, HTMLResponse
from templating.jinja_template import templates

router = APIRouter()

UPLOADS_DIR = Path("uploads")


@router.get("/", name="programs:list", response_class=HTMLResponse)
def list_view(
    request: Request,
    storage: GetProgramsStorage,
) -> HTMLResponse:
    context: dict[str, Any] = {}
    programs = storage.get()
    context.update(programs=programs)
    return templates.TemplateResponse(
        request=request,
        name="programs/list.html",
        context=context,
    )


@router.get(
    "/{name}/",
    name="program:get",
    dependencies=[Depends(validate_basic_auth)],
)
def get_program(
    program: ProgramByName,
) -> FileResponse:
    return FileResponse(
        path=UPLOADS_DIR / f"{program.name}.zip",
        filename=f"{program.name}.zip",
    )
