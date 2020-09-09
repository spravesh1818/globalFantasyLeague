from datetime import timedelta
from typing import List

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from starlette import status

from authenticationUtils import (
    get_current_active_user,
    get_password_hash,
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
)
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from .users_schema import User, UserCreate
from .users_model import users
from db import database


router = APIRouter()


@router.post("/token")
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
        {"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users", response_model=List[User])
async def read_items(current_user: User = Depends(get_current_active_user)):
    output: List[User] = []
    query = users.select()
    rows = await database.fetch_all(query=query)
    for row in rows:
        output.append(User(**row))

    return output


@router.post("/register", response_model=User)
async def create_user(user: UserCreate):
    try:
        user.password = get_password_hash(user.password)
        query = users.insert().values(
            username=user.username,
            email=user.email,
            password=user.password,
            full_name=user.full_name,
            disabled=user.disabled,
            role=user.role,
        )
        last_record_id = await database.execute(query)
        return {**user.dict(), "id": last_record_id}
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
