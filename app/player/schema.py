from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Position(str, Enum):
    fwd = "forward"
    mfd = "midfielder"
    dfd = "defender"
    gk = "goalkeeper"


class Player(BaseModel):
    name: str
    nationality: str
    kit_no: int
    position: Position
    dominant_foot: Optional[str] = None

    class Config:
        orm_mode = True
