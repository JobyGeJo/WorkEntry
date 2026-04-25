import re
from datetime import date, time
from typing import Optional, Self
from pydantic import BaseModel, constr, field_validator, model_validator
from Enums import Roles


class LoginPayload(BaseModel):
    username: str
    password: str

class UpdateRolesPayload(BaseModel):
    role: Roles

class RegisterPayload(BaseModel):
    full_name: str
    username: str
    password: str
    phone_number: Optional[constr(pattern=r"^\+?\d{10,15}$")] = None

    @field_validator("full_name")
    def validate_full_name(cls, v):
        if len(v) < 3:
            raise ValueError("Full name must be at least 3 characters long")
        if not re.search(r"^[A-Za-z ]+$", v):
            raise ValueError("Username must only contain letters")
        return v.title()

    @field_validator("username")
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if not re.search(r"^[A-Za-z ]+$", v):
            raise ValueError("Username must only contain letters")
        return v.lower()

    # noinspection PyMethodParameters
    @field_validator("password")
    def validate_password(cls, v): # keep 'cls', not 'self'
        # Require at least one digit and one special character
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"\d", v):
            raise ValueError("Password must include at least one number")
        if not re.search(r"[!@#$%^&*()_+-=,.?\":{}|<>]", v):
            raise ValueError("Password must include at least one special character")
        return v

class PhoneNumberUpdatePayload(BaseModel):
    phone_id: int
    phone_number: Optional[str]
    type: Optional[str] = None

class EmailUpdatePayload(BaseModel):
    email_id: int
    email: str = None

class AddressUpdatePayload(BaseModel):
    address_id: int
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    type: Optional[str] = None

class UserUpdatePayload(BaseModel):
    full_name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None

    phone_number: Optional[PhoneNumberUpdatePayload] = None
    email: Optional[EmailUpdatePayload] = None
    address: Optional[AddressUpdatePayload] = None

class TimesheetPayload(BaseModel):
    user_id: Optional[int] = None
    machine: Optional[str]
    description: str
    date: date
    start_time: time
    end_time: time

    @model_validator(mode="after")
    def check_time_order(self) -> Self:
        if self.start_time >= self.end_time:
            raise ValueError("start_time must be earlier than end_time")
        return self