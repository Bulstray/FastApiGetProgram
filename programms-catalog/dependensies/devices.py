from typing import Annotated, cast

from fastapi import Depends, HTTPException, Request, status
from schemas.devices.devices import Device
from storage.devices.crud import DeviceStorage


def get_device_storage(request: Request) -> DeviceStorage:
    return cast(DeviceStorage, request.app.state.devices_storage)


GetDevicesStorage = Annotated[
    DeviceStorage,
    Depends(get_device_storage),
]


def prefetch_device_by_name(
    name: str,
    storage: GetDevicesStorage,
) -> Device:
    program: Device | None = storage.get_by_name(name=name)

    if program:
        return program

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Program not found",
    )


DeviceByName = Annotated[Device, Depends(prefetch_device_by_name)]


data = {
    "seis": {
        "span": "Сейсмическое оборудование",
        "title": "Приборы сейсморазведки",
        "description": "Профессиональное оборудование для современных сейсмических исследований. Высокоточные приборы и системы для полевых работ и лабораторных исследований.",
    },
    "grav": {
        "span": "Гравиаметрическое оборудование",
        "title": "Приборы гравиаразведки",
        "description": "Современные гравиметры и системы гравиразведки для высокоточных измерений вариаций силы тяжести. Оборудование для полевых исследований, лабораторных измерений и мониторинга гравитационных аномалий.",
    },
}


def prefetch_devices_by_type(
    type_device: str,
    storage: GetDevicesStorage,
) -> dict:
    context = dict(**data[type_device])
    devices = [device for device in storage.get() if device.type_device == type_device]

    context.update(devices=devices)
    return context


DeviceByType = Annotated[dict, Depends(prefetch_devices_by_type)]
