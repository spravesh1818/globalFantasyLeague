from datetime import timedelta
from typing import List
from loguru import logger

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
from .schema import User, UserCreate
from .models import users
from db import database


router = APIRouter()


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        logger.error("User authentication failed")
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

    logger.info("All users fetched")
    return output


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int, current_user: User = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        logger.error("User Authorization failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED"
        )

    query = users.delete().where(users.c.id == user_id)
    response = await database.execute(query)
    logger.info("Response from the server {}".format(response))
    return {"msg": "User deleted successfully"}


@router.put("/users/{user_id}")
def edit_user(
    user_id: int, userData: User, current_user: User = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED"
        )

    # TODO:edit the row


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
        logger.info("User {} registered successfully".format(user.username))
        return {**user.dict(), "id": last_record_id}
    except IntegrityError as e:
        logger.info("User with same username or email already exists")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
