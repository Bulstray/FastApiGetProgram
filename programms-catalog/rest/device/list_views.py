from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from fastapi.staticfiles import StaticFiles

from dependensies.devices import DeviceByType
from templating.jinja_template import templates


router = APIRouter()

router.mount("/uploads", StaticFiles(directory="uploads"), name="uploads-static")


@router.get("/{type_device}/", name="devices:list", response_class=HTMLResponse)
def list_view(request: Request, devices: DeviceByType):
    devices.update(static_prefix="/uploads")
    return templates.TemplateResponse(
        request=request,
        name="devices/list.html",
        context=devices,
    )
