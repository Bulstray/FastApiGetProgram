class DevicesBaseError(Exception):
    """Base exception for program CRUD actions."""


class DevicesAlreadyExistsError(DevicesBaseError):
    """Raised on program if such slug already exists."""


class UnsupportedFormatFileError(Exception):
    """Raised if the file format is unsupported"""
