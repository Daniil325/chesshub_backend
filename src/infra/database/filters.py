import abc
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum, auto
import operator
import re
from typing import Any, ClassVar
from urllib.parse import parse_qsl

from sqlalchemy import (
    Executable,
    Table,
    and_,
    not_,
    or_,
)

from src.infra.exceptions import FieldNotFound


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


IdentityOperators = {Operator.Equal, Operator.NotEqual}

OrderOperators = {
    Operator.Greater,
    Operator.GreaterOrEqual,
    Operator.Less,
    Operator.LessOrEqual,
}

NumberOperators = IdentityOperators | OrderOperators

TextualOperators = {Operator.StartWiths, Operator.EndWiths, Operator.Contain}


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


@dataclass
class FilterType(abc.ABC):
    operators: ClassVar[set[Operator]]

    @abc.abstractmethod
    def validate(self, value: Any) -> Any: ...


@dataclass
class IntFilterType(FilterType):
    operators = NumberOperators

    def prepare_value(self, value: Any) -> Any:
        return int(value)


@dataclass
class BoolFilterType(FilterType):
    operators = IdentityOperators

    def validate(self, value: Any) -> Any:
        if isinstance(value, (bool, int)):
            return bool(value)
        if isinstance(value, str):
            result = {
                "1": True,
                "yes": True,
                "true": True,
                "on": True,
                "0": False,
                "no": False,
                "false": False,
                "off": False,
            }.get(value.lower().strip())
            if result is not None:
                return result
        raise ValueError(f'Bad value for bool "{value}"')


@dataclass
class StringFilterType(FilterType):
    operators = IdentityOperators | OrderOperators | TextualOperators

    def validate(self, value: Any) -> str:
        return str(value)


@dataclass
class DataTimeFilter(FilterType):
    operators = NumberOperators
    format: str | None = None

    def validate(self, value: Any) -> Any:
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value)
        if isinstance(value, str):
            if self.format:
                return datetime.strptime(value, self.format)
            else:
                return datetime.fromisoformat(value)
        raise ValueError(f'Bad value for bool "{value}"')


class OrderDirection(IntEnum):
    Ascending = 1
    Descending = -1


@dataclass(frozen=True, slots=True)
class Order:
    field: Field
    direction: OrderDirection


@dataclass(frozen=True, slots=True)
class FilterLogic:
    operator: LogicOperator
    filters: list["Filter"] = field(default_factory=list)


class WhereQuery:
    field_pattern = re.compile(r"(?P<name>[^[]+)(\[(?P<op>[^[]+)])?", re.UNICODE)
    operators: dict[str, Operator] = {
        "eq": Operator.Equal,
        "ne": Operator.NotEqual,
        "gt": Operator.Greater,
        "gte": Operator.GreaterOrEqual,
        "lt": Operator.Less,
        "lte": Operator.LessOrEqual,
        "start": Operator.StartWiths,
        "end": Operator.EndWiths,
        "like": Operator.Contain,
    }

    def __init__(self):
        self._order = []
        self._filter = []

    def __call__(self, filter_string: str, order_by_string: str):
        self.parse_sort(order_by_string)
        for left, right in parse_qsl(filter_string):
            self.parse_filter(left, right)
        return [self._filter, self._order]

    def parse_filter(self, left: str, right: str):
        match = self.field_pattern.fullmatch(left)
        operator_name = match.group("op") or "eq"
        operator = self.operators.get(operator_name)
        # TODO: сделать нормальное преобразование типов(изначально любое значение - строка)
        if right.isdigit():
            right = int(right)
        elif datetime.strptime(right, "%Y-%m-%d"):
            right = datetime.strptime(right, "%Y-%m-%d")
        self._filter.append(
            ValueFilter(field=match.group("name"), operator=operator, value=right)
        )

    def parse_sort(self, value: str):
        for field in value.split(","):
            f = field.strip()
            if not f:
                continue
            direction = (
                OrderDirection.Descending
                if f[0] == "-" or f[-1] == "-"
                else OrderDirection.Ascending
            )
            self._order.append(
                Order(field=f.lstrip("-+").rstrip("-+"), direction=direction)
            )

    def build_pagination(self): ...


class SqlAlchemyBuilder:
    def __init__(self, table: Table, base_stmt):
        self.table = table
        self.query_string_parser = WhereQuery()
        self.base_stmt = base_stmt
        self.stack = deque()

    @property
    def statement(self) -> Executable:
        filter = self.sql_filter
        order = self.sql_sort
        self.base_stmt = self.base_stmt.where(and_(*filter)).order_by(*order)
        return self.base_stmt

    def __call__(self, filter_string: str, order_by_string: str):
        filter, order = self.query_string_parser(filter_string, order_by_string)
        self.sql_filter = self.convert_to_sql_condition(filter)
        self.sql_sort = self.convert_to_sql_order(order)
        return self.statement

    def convert_to_sql_condition(self, filter: list[ValueFilter]):
        result = []
        for item in filter:
            field = item.field
            operator = operator_map[item.operator]
            value = item.value
            db_name = self.get_db_name(self.table, field)
            result.append(operator(db_name, value))
        return result

    def exit_filter(self):
        if len(self.stack) > 0:
            nested = self.stack.pop()
            self.sql_filter = nested
        else:
            self.sql_filter = True

    def convert_to_sql_order(self, order: list[Order]):
        result = []
        for item in order:
            field = item.field
            db_name = self.get_db_name(self.table, field)
            if item.direction == -1:
                sort_func = db_name.asc
            else:
                sort_func = db_name.desc
            result.append(sort_func())
        return result

    def get_db_name(self, table: Table, filter_name: str) -> str:
        if filter_name not in table.columns.keys():
            raise FieldNotFound(
                "Table {} has no column `{}`.".format(table, filter_name)
            )
        return table.c[filter_name]
