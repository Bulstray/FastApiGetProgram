from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, UploadFile, status
from schemas.devices.devices import Device, DeviceCreate
from storage.devices.crud import storage
from storage.devices.exceptions import (
    DevicesAlreadyExistsError,
    UnsupportedFormatFileError,
)

router = APIRouter()


@router.get(
    "/",
)
def read_device_list() -> list[Device]:
    return storage.get()


@router.post("/", response_model=Device, status_code=status.HTTP_201_CREATED)
def add_device(
    type_device: Annotated[str, Form(...)],
    name: Annotated[str, Form(...)],
    description: Annotated[str, Form(...)],
    picture: UploadFile,
    instruction: UploadFile,
) -> Device | None:
    try:
        create_device = DeviceCreate(
            name=name,
            description=description,
            type_device=type_device,
        )
        return storage.create_or_raise_if_exists(
            device_in=create_device,
            picture=picture,
            instruction=instruction,
        )

    except DevicesAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Device with name={name!r} already exists",
        )

    except UnsupportedFormatFileError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Invalid file format picture={picture.filename!r} or instruction={instruction.filename!r}",
        )
