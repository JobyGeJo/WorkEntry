# request.py
import re
from datetime import datetime, date
from typing import Optional, List

from Exceptions import BadRequest
from pydantic import BaseModel, Field, constr, field_validator

from database.tables import UserTable, TimesheetTable
from models.models import TimeSheet


class LoginPayload(BaseModel):
    id: int
    password: str

class RegisterPayload(BaseModel):
    username: constr(pattern=r"^[A-Za-z]+$")  # Only letters, no digits/symbols
    password: constr(min_length=8)
    phone_number: Optional[constr(pattern=r"^\+?\d{10,15}$")] = None

    # noinspection PyMethodParameters
    @field_validator("password")
    def validate_password(cls, v): # keep 'cls', not 'self'
        # Require at least one digit and one special character
        if not re.search(r"\d", v):
            raise ValueError("Password must include at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must include at least one special character")
        return v

class QueryParams(BaseModel):
    skip: int = Field(0, ge=0)
    limit: int = Field(10, ge=1)
    # sort_by: Optional[str] = "created_at"
    # order: Optional[str] = "asc"
    search: Optional[str] = None

    def execute(self, base_query) -> List:
        return self.build(base_query).all()

    def build[T](self, base_query: T) -> T:
        return base_query.offset(self.skip).limit(self.limit)


class TimeSheetParams(QueryParams):
    machine: Optional[str] = None
    person: Optional[str] = None
    description: Optional[str] = None
    from_date: date = date.today()
    to_date: date = date.today()

    def build[T](self, base_query: T) -> T:
        query = base_query

        query = query.filter(
            TimesheetTable.start_time >= self.from_date,
            TimesheetTable.start_time <= datetime.combine(self.to_date, datetime.max.time())
        )

        if self.person:
            query = query.filter(UserTable.username.ilike(f"%{self.person}%"))
        if self.machine:
            query = query.filter(TimesheetTable.machine_name.ilike(f"%{self.machine}%"))
        if self.description:
            query = query.filter(TimesheetTable.description.ilike(f"%{self.description}%"))

        return super().build(query)

    def execute(self, base_query) -> List[TimeSheet]:
        return self.build(base_query).all()
