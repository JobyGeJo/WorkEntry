from datetime import datetime, date
from typing import Optional, Literal, Self, Callable, Any

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator, model_validator, PrivateAttr
from sqlalchemy import Column, BinaryExpression, ColumnElement
from sqlalchemy.orm import Query as SQLQuery

from database.postgres.tables import UserTable, TimesheetTable
from models.response import Pagination


class QueryParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1)

    _pagination: Optional[Pagination] = PrivateAttr(None)

    _filters: dict[str, Callable] = {}

    @property
    def pagination(self):
        return self._pagination

    def apply_filters(self, base_query: SQLQuery) -> SQLQuery:
        """Apply all defined filters from _filters dict."""
        query = base_query
        for attr, condition_fn in self._filters.items():
            value = getattr(self, attr, None)
            if value is not None:
                query = query.filter(condition_fn(value))
        return query

    def apply_sort(self, query: SQLQuery) -> SQLQuery:
        if self.sort_by:
            query = query.order_by(self.sort_by)
        return query

    def build(self, base_query: SQLQuery) -> SQLQuery:
        query = self.apply_filters(base_query)
        query = self.apply_sort(query)
        self._pagination = Pagination(total_items=query.count(), limit=self.limit, page=self.page)
        return base_query.offset((self.page - 1) * self.limit).limit(self.limit)

    @staticmethod
    def eq(column: Column) -> Callable[[Any], ColumnElement[bool]]:
        return lambda value: column == value

    # noinspection SpellCheckingInspection
    @staticmethod
    def ilike(column: Column) -> Callable[[Any], BinaryExpression[bool]]:
        return lambda value: column.ilike(f"%{value}%")

class UserParams(QueryParams):
    username: Optional[str] = None
    phone_number: Optional[str] = None
    role_id: Optional[int] = None

    sort_by: Optional[Literal["username"]] = None

    _filters = {
        "username": QueryParams.ilike(UserTable.username),
        "phone_number": QueryParams.ilike(UserTable.phone_number),
        "role_id": QueryParams.eq(UserTable.role_id)
    }

    # noinspection PyMethodParameters
    @field_validator("sort_by")
    def validate_sort_by(cls, v):
        if v is None:
            return None

        match v:
            case "username":
                return UserTable.username
            case _:
                raise ValueError(f"Invalid sort_by value: {v!r}")

class TimeSheetParams(QueryParams):
    user_id: Optional[int] = None
    machine: Optional[str] = None
    description: Optional[str] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None

    sort_by: Optional[Literal["machine", "start_time", "end_time"]] = None

    _filters = {
        "user_id": QueryParams.eq(TimesheetTable.user_id),
        "machine": QueryParams.ilike(TimesheetTable.machine_name),
        "description": QueryParams.ilike(TimesheetTable.description)
    }

    @model_validator(mode="after")
    def check_date(self) -> Self:
        if self.from_date or self.to_date:
            self.from_date = self.from_date or date.today()
            self.to_date = self.to_date or date.today()

            if self.from_date > self.to_date:
                raise RequestValidationError([
                    {
                        "loc": ("query", "from_date"),
                        "msg": "from_date must be earlier than to_date",
                        "type": "value_error"
                    }
                ])

        return self

    # noinspection PyMethodParameters
    @field_validator("sort_by")
    def validate_sort_by(cls, v):
        if v is None:
            return None

        match v:
            case "machine":
                return TimesheetTable.machine_name
            case "start_time":
                return TimesheetTable.start_time
            case "end_time":
                return TimesheetTable.end_time
            case _:
                raise ValueError(f"Invalid sort_by value: {v!r}")

    def build(self, base_query: SQLQuery) -> SQLQuery:
        query = base_query
        if self.from_date and self.to_date:
            query = base_query.filter(
                TimesheetTable.start_time >= self.from_date,
                TimesheetTable.start_time <= datetime.combine(self.to_date, datetime.max.time())
            )
        return super().build(query)
