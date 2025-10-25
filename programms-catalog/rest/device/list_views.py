from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from fastapi.responses import FileResponse
from starlette.staticfiles import StaticFiles

from dependensies.devices import DeviceByType
from templating.jinja_template import templates

from pathlib import Path


router = APIRouter()


@router.get("/{type_device}/", name="devices:list", response_class=HTMLResponse)
def list_view(request: Request, devices: DeviceByType):
    return templates.TemplateResponse(
        request=request,
        name="devices/list.html",
        context=devices,
    )


# /devices/grav/uploads/device/grav/string/L5OiGC25Bp9EaqN1KVIM.jpg
# /devices/grav/L5OiGC25Bp9EaqN1KVIM.jpg


@router.get("/{type_device}/{name}/{picture}", name="picture:get")
def get_picture(request: Request, type_device: str, name: str, picture: str):
    return FileResponse(f"uploads/device/{type_device}/{name}/{picture}")
