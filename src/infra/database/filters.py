from dataclasses import dataclass
from enum import IntEnum, auto
import operator
from typing import Any

from sqlalchemy import and_, not_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.sqla_repo import SqlHelper
from src.domain.article.entities import Article


type Field = str


class Operator(IntEnum):
    # equality
    Equal = auto()
    NotEqual = auto()
    # order
    Greater = auto()
    GreaterOrEqual = auto()
    Less = auto()
    LessOrEqual = auto()
    # textual
    StartWiths = auto()
    EndWiths = auto()
    Contain = auto()


@dataclass(frozen=True, slots=True)
class ValueFilter:
    field: Field
    operator: Operator
    value: Any


class LogicOperator(IntEnum):
    And = auto()
    Or = auto()
    Not = auto()


operator_map = {
    Operator.Equal: operator.eq,
    Operator.NotEqual: operator.neg,
    Operator.Greater: operator.gt,
    Operator.GreaterOrEqual: operator.ge,
    Operator.Less: operator.lt,
    Operator.LessOrEqual: operator.le,
    Operator.Contain: lambda field, value: field.contains(value),
}

logic_map = {
    LogicOperator.And: and_,
    LogicOperator.Or: or_,
    LogicOperator.Not: not_,
}


class FilterQuery:

    def __init__(self): ...

    @property
    def statement(self): ...

    def parse_where(self): ...

    def parse_sort(self): ...

    def build_pagination(self): ...


class BaseReader:

    def __init__(self, session: AsyncSession, model) -> None:
        super().__init__(session, model)
        self.model = model

    async def fetch_list(self, page, per_page, filter, order):
        stmt = select(self.model)
        prepared_where = FilterQuery().statement


class ArticleReader:

    async def fetch_list(self, page, per_page, filter, order):
        stmt = select(Article)
