from typing import List

from sqlalchemy.exc import IntegrityError
from starlette import status

from authenticationUtils import get_current_active_user, get_password_hash
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from .users_schema import User, UserCreate
from .users_model import users
from db import database


router = APIRouter()


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
