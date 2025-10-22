from typing import Any

from dependensies.programs import GetProgramsStorage
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, FileResponse
from templating.jinja_template import templates
from dependensies.programs import ProgramByName
from pathlib import Path

from dependensies.auth import validate_basic_auth

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
