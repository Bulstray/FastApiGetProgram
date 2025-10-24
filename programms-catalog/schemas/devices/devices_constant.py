from typing import Annotated

from annotated_types import Len, MaxLen
from pydantic import AfterValidator

DESCRIPTION_MAX_LENGTH = 500

NAME_MAX_LENGTH = 50
NAME_MIN_LENGTH = 3


NameString = Annotated[str, Len(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH)]
DescriptionString = Annotated[str, MaxLen(DESCRIPTION_MAX_LENGTH)]


def validate_type_device(type_device: str):
    if type_device.lower() not in ("grav", "mag", "seis"):
        raise ValueError(f"{type_device} is not a valid type")

    return type_device


TypeDeviceString = Annotated[str, AfterValidator(validate_type_device)]
