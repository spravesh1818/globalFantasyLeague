from typing import List
import sqlalchemy
from sqlalchemy.orm import Session, scoped_session
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import JWTError, jwt
from _sqlite3 import IntegrityError

import models
from schemas import UserCreate,User
from database import engine, SessionLocal
import crud



#databases database
from db import engine as eg
from db import database as adb,metadata
from db_models import league,users




SECRET_KEY = "8ee7b057761c29f8ca0a336f850aa73abf9eeb81c6a5b015c893af74d7e6a948"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


models.Base.metadata.create_all(bind=engine)
metadata.create_all(eg)

app = FastAPI()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

'''Code for oauth implementation'''


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(username: str):
    query = users.select()
    user_list=await adb.fetch_all(query)
    for user in user_list:
        if user.username == username:
            return user
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


'''authenticating user'''
# TODO:change the fake db implementation to real db


async def authenticate_user(username: str, password: str):
    user =await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


'''code to create the access token'''


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now()+expires_delta
    else:
        expire = datetime.utcnow()+timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


'''getting the current user details'''


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if not user:
        raise credentials_exception
    return user

'''Checking users if they are active or not'''


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

'''Oauth token url.All the logic behind authentication goes here'''


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        {"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}



@app.on_event("startup")
async def startup():
    await adb.connect()
    print("connected to the db")


@app.on_event("shutdown")
async def shutdown():
    await adb.disconnect()
    print("disconnected from the db")

'''All the routes are stored here'''

class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool

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


@app.get("/users", response_model=List[User])
async def read_items(db=Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return crud.get_all_users(db)


@app.post("/register", response_model=User)
async def create_user(user:UserCreate, db=Depends(get_db)):
    try:
        user.password = get_password_hash(user.password)
        query=users.insert().values(username=user.username,email=user.email,hashed_password=user.password,full_name=user.full_name,disabled=user.disabled,role=user.role)
        last_record_id=await adb.execute(query)
        return {**user.dict(),"id":last_record_id}
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=str(e))


# @app.get("/leagues", response_model=List[schemas.League])
# def read_leagues(skip: int = 0, limit: int = 0, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
#     leagues = crud.get_leagues(db, skip=skip, limit=limit)
#     print(leagues)
#     return leagues
#
#
# @app.post("/leagues", response_model=schemas.LeagueCreate)
# def write_leagues(league: schemas.LeagueCreate, db=Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
#     return crud.create_league(db, league)
#
#
# @app.get("/leagues/{league_id}", response_model=schemas.LeagueCreate)
# def read_league(league_id: int, db=Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
#     return crud.get_league(db, league_id)
#
#
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
