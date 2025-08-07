# request.py
import re
from typing import Optional, List

from Exceptions import BadRequest
from pydantic import BaseModel, Field, constr, field_validator


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

    def execute(
            self,
            base_query,  # pre-built query (can include joins)
            search_column=None  # e.g., VendorTable.name
    ) -> List:
        query = base_query

        if self.search and search_column is not None:
            search_filter = search_column.ilike(f"%{self.search}%")
            query = query.filter(search_filter)

        query = query.offset(self.skip).limit(self.limit)
        return query.all()
