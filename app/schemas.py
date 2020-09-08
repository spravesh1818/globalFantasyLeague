from typing import Optional, List
from pydantic import BaseModel
from enum import Enum


class Role(str, Enum):
    user = "user"
    admin = "admin"


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


class Team(BaseModel):
    name: str
    nickname: Optional[str] = None
    stadium: Optional[str] = None
    owner: Optional[str] = None

    class Config:
        orm_mode = True


class TeamCreate(Team):
    players: List[Player] = []


class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    role: Role

    class Config:
        orm_mode = True


class UserCreate(User):
    password: str

    class Config:
        orm_mode = True


class League(BaseModel):
    name: str
    country: str
    division: str

    class Config:
        orm_mode = True


class LeagueCreate(League):
    teams: List[Team] = []
