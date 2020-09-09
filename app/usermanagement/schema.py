from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Role(str, Enum):
    user = "user"
    admin = "admin"


class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    role: Role


class UserCreate(User):
    password: str
