from datetime import datetime, date, time
from typing import Optional, List

from pydantic import BaseModel, PrivateAttr, Field

from Enums import Roles


class __default_model(BaseModel):
    model_config = {
        "from_attributes": True,
    }

class User(__default_model):
    user_id: int
    full_name: str
    dob: Optional[date]
    gender: Optional[str]
    # created_at: datetime
    # updated_at: datetime
    
class UserWithRole(User):
    role: Roles
    
class PhoneNumber(__default_model):
    phone_id: int
    phone_number: str
    type: Optional[str]
    is_primary: bool = False
    
class Email(__default_model):
    email_id: int
    email: str
    is_primary: bool = False
    
class Address(__default_model):
    address_id: int
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    country: str
    postal_code: str
    type: str
    is_primary: bool = False

class UserDetails(UserWithRole):
    phone_numbers: List[PhoneNumber]
    emails: List[Email]
    addresses: List[Address]

class Timesheet(__default_model):
    id: int
    user_id: int
    person: str
    machine: str
    description: Optional[str]
    remark: Optional[str]
    reviewed_by: Optional[int]
    date: date
    start_time: time
    end_time: time

class TimesheetWithUser(Timesheet):
    user: User
    user_id: int = Field(..., exclude=True)