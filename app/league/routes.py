from typing import List

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from authenticationUtils import get_current_active_user
from starlette import status
from usermanagement.schema import User
from sqlalchemy import select
from db import database

from .schema import League
from .models import league


router = APIRouter()


@router.get("/leagues/{league_id}", response_model=League)
async def read_league(
    league_id: int, current_user: User = Depends(get_current_active_user)
):
    query = select([league]).where(league.c.id == league_id)
    row = await database.fetch_one(query)
    return League(**row)


@router.get("/leagues", response_model=List[League])
async def read_leagues(
    skip: int = 0, limit: int = 0, current_user: User = Depends(get_current_active_user)
):

    output: List[League] = []
    query = league.select()
    rows = await database.fetch_all(query=query)
    for row in rows:
        output.append(League(**row))

    return output


#
@router.post("/leagues", response_model=League)
async def write_leagues(
    leagueModel: League, current_user: User = Depends(get_current_active_user)
):
    query = league.insert().values(name=leagueModel.name, division=leagueModel.division)
    last_record_id = await database.execute(query)
    return {**leagueModel.dict(), "id": last_record_id}


@router.delete("/leagues/{league_id}")
async def delete_league(
    league_id: int, current_user: User = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED"
        )
    query = league.delete().where(league.c.id == league_id)
    await database.execute(query)
    return {"msg": "Record deleted successfully"}
