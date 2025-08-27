from datetime import datetime, date, time
from typing import Optional

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

class UserDetail(User):
    role: Roles

class Timesheet(__default_model):
    id: int
    user_id: int
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