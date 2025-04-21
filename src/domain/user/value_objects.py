from dataclasses import dataclass
from src.domain.user.exceptions import FullUserNameException


@dataclass
class FullUserName:
    _name: str
    _surname: str

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if len(value) == 0:
            raise FullUserNameException
        self._name = value.capitalize()

    @property
    def surname(self) -> str:
        return self._surname

    @surname.setter
    def surname(self, value: str) -> None:
        if len(value) == 0:
            raise FullUserNameException
        self._surname = value.capitalize()
