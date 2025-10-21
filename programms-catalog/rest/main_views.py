from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from templating.jinja_template import templates

router = APIRouter(include_in_schema=False)


@router.get("/", name="home")
def read_docs(request: Request) -> HTMLResponse:
    context: dict[str, Any] = {}

    features = [
        "Add new program",
        "Load program",
        "Update program",
        "Delete program",
    ]

    context.update(
        features=features,
    )

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context=context,
    )
