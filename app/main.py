from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from league import league_routes
from usermanagement import users_routes

# databases database
from db import database as adb

from usermanagement.users_model import users

from authenticationUtils import authenticate_user, create_access_token

SECRET_KEY = "8ee7b057761c29f8ca0a336f850aa73abf9eeb81c6a5b015c893af74d7e6a948"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await adb.connect()


@app.on_event("shutdown")
async def shutdown():
    await adb.disconnect()


# @app.get("/notes/", response_model=List[Note])
# async def read_notes():
#     query = notes.select()
#     return await adb.fetch_all(query)
#
#
# @app.post("/notes/", response_model=Note)
# async def create_note(note: NoteIn):
#     query = notes.insert().values(text=note.text, completed=note.completed)
#     last_record_id = await adb.execute(query)
#     return {**note.dict(), "id": last_record_id}


# @app.post("/players", response_model=schemas.Player)
# def write_player_info(player: schemas.Player, db=Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
#     return crud.create_player(db, player)
#
#
# @app.get("/players", response_model=List[schemas.Player],)
# def get_all_players(db=Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
#     return crud.get_all_players(db)
#
#
# @app.get("/players/{player_id}", response_model=schemas.Player)
# def get_player_info(player_id: int, db=Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
#     return crud.get_player(db, player_id)
#
#
# @app.post("/teams", response_model=schemas.Team)
# def write_team_info(team: schemas.TeamCreate, db=Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
#     return crud.create_team(db, team)
#
#
# @app.get("/teams", response_model=List[schemas.Team])
# def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends((get_db)), current_user: schemas.User = Depends(get_current_active_user)):
#     teams = crud.get_teams(db, skip=skip, limit=limit)
#     return teams
#
#
# @app.get("/teams/{team_id}", response_model=schemas.Team)
# def read_team(team_id: int, db: Session = Depends((get_db)), current_user: schemas.User = Depends(get_current_active_user)):
#     return crud.get_team(db, team_id)

app.include_router(league_routes.router, tags=["League"])
app.include_router(users_routes.router, tags=["User Management"])


if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8000, reload=True, access_log=False)
