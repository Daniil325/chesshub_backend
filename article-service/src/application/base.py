from abc import ABC, abstractmethod
from dataclasses import dataclass


class IFacade(ABC):
    @abstractmethod
    def execute(self): ...


@dataclass
class DTO(ABC): ...


class ICommand(ABC):
    @abstractmethod
    def __init__(self, dto: DTO, repo): ...

    @abstractmethod
    async def handle(self, dto): ...


class IQuery(ABC):
    @abstractmethod
    async def fetch_list(self, filter: str, page: int, per_page: int) -> list: ...

    @abstractmethod
    async def get_by_id(self, id: str | int): ...


class ICommandService(ABC):
    @abstractmethod
    async def create(self, item: DTO) -> None: ...

    @abstractmethod
    async def update(self, id: str | int, changes: DTO) -> None: ...

    @abstractmethod
    async def delete(self, id: str | int) -> None: ...
