from typing import Optional, List

from pydantic import BaseModel
from player.player_schema import Player


class Team(BaseModel):
    name: str
    nickname: Optional[str] = None
    stadium: Optional[str] = None
    owner: Optional[str] = None

    class Config:
        orm_mode = True


class TeamCreate(Team):
    players: List[Player] = []
