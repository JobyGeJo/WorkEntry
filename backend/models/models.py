from typing import Optional

from pydantic import BaseModel


class __default_model(BaseModel):
    model_config = {
        "from_attributes": True,
    }

class User(__default_model):
    id: int
    username: str
    phone_number: Optional[str] = None