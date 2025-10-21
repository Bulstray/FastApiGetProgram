from typing import Any

from dependensies.programs import GetProgramsStorage
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from templating.jinja_template import templates

router = APIRouter()


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
