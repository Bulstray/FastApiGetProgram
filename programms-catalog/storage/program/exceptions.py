class ProgramBaseError(Exception):
    """Base exception for program CRUD actions."""


class ProgramAlreadyExistsError(ProgramBaseError):
    """Raised on program if such slug already exists."""


class UnsupportedFormatFileError(Exception):
    """Raised if the file format is unsupported"""
