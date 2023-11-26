class ParserError(Exception):
    def __init__(self, message: str) -> None:
        self._msg = message

    def __str__(self) -> str:
        return self._msg
