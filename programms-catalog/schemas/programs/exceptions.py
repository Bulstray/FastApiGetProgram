class UnsupportedFormatFileError(Exception):
    def __init__(self) -> None:
        super().__init__("Unsupported file format")
