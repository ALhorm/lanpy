class Token:
    def __init__(self, name: str, value: str) -> None:
        self._name = name
        self._value = value

    def __str__(self) -> str:
        return f'Token({self._name}, "{self._value}")'

    def __repr__(self) -> str:
        return f'Token({self._name}, "{self._value}")'

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> str:
        return self._value
