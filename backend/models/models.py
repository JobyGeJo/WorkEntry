from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class __default_model(BaseModel):
    model_config = {
        "from_attributes": True,
    }

class User(__default_model):
    id: int
    username: str
    role_id: int
    phone_number: Optional[str] = None

class TimeSheet(__default_model):
    id: int
    person: str
    machine: str
    description: str
    start_time: datetime
    end_time: datetime