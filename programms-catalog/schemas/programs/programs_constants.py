from typing import Annotated

from annotated_types import Len, MaxLen

# Limitations for the scheme
NAME_MIN_LENGTH = 3
NAME_MAX_LENGTH = 50

DESCRIPTION_MAX_LENGTH = 500


# String types with length constraints for the schema
NameString = Annotated[
    str,
    Len(
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_MAX_LENGTH,
    ),
]

DescriptionString = Annotated[str, MaxLen(DESCRIPTION_MAX_LENGTH)]
