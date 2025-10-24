from fastapi import APIRouter, status

from dependensies.devices import GetDevicesStorage, DeviceByName


router = APIRouter()


@router.delete(
    "/{name}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_program_by_name(
    program: DeviceByName,
    storage: GetDevicesStorage,
) -> None:
    storage.delete_by_name(name=program.name)
