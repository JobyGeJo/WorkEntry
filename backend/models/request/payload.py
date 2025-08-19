import re
from datetime import datetime
from typing import Optional, Self

from pydantic import BaseModel, constr, field_validator, model_validator


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
        if not re.search(r"[!@#$%^&*()_+-=,.?\":{}|<>]", v):
            raise ValueError("Password must include at least one special character")
        return v

class TimesheetPayload(BaseModel):
    user_id: Optional[int] = None
    machine: Optional[str]
    description: str
    start_time: datetime
    end_time: datetime

    @model_validator(mode="after")
    def check_time_order(self) -> Self:
        if self.start_time >= self.end_time:
            raise ValueError("start_time must be earlier than end_time")
        return self