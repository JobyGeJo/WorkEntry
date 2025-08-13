from datetime import datetime, date
from typing import Optional, Literal, Self

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator, model_validator, PrivateAttr
from sqlalchemy.orm import Query as SQLQuery

from database.postgres.tables import UserTable, TimesheetTable
from models.response import Pagination


class QueryParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1)

    _pagination: Optional[Pagination] = PrivateAttr(None)

    def build(self, base_query: SQLQuery) -> SQLQuery:
        self._pagination = Pagination(total_items=base_query.count(), limit=self.limit, page=self.page)
        return base_query.offset((self.page - 1) * self.limit).limit(self.limit)

    @property
    def pagination(self):
        return self._pagination

class UserParams(QueryParams):
    username: Optional[str] = None
    phone_number: Optional[str] = None
    role_id: Optional[int] = None

    sort_by: Optional[Literal["username"]] = None

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

    def build(self, base_query: SQLQuery) -> SQLQuery:
        query = base_query

        if self.role_id:
            query = query.filter(UserTable.id == self.role_id)
        if self.username:
            query = query.filter(UserTable.username.ilike(f"%{self.username}%"))
        if self.phone_number:
            query = query.filter(UserTable.phone_number.ilike(f"%{self.phone_number}%"))

        if self.sort_by:
            query = query.order_by(self.sort_by)

        return super().build(query)

class TimeSheetParams(QueryParams):
    user_id: Optional[int] = None
    machine: Optional[str] = None
    description: Optional[str] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None

    sort_by: Optional[Literal["machine", "start_time", "end_time"]] = None

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
            query = query.filter(
                TimesheetTable.start_time >= self.from_date,
                TimesheetTable.start_time <= datetime.combine(self.to_date, datetime.max.time())
            )

        if self.user_id:
            query = query.filter(UserTable.id == self.user_id)
        if self.machine:
            query = query.filter(TimesheetTable.machine_name.ilike(f"%{self.machine}%"))
        if self.description:
            query = query.filter(TimesheetTable.description.ilike(f"%{self.description}%"))

        if self.sort_by:
            query = query.order_by(self.sort_by)

        return super().build(query)
