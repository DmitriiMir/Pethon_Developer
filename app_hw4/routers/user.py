from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app_hw4.backend.db_depends import get_db
from typing import Annotated
from app_hw4.models.user import User
from app_hw4.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter()


@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

@router.get("/{user_id}")
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

@router.post("/create")
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    slug = slugify(user.username)
    stmt = insert(User).values(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        slug=slug
    )
    db.execute(stmt)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put("/update/{user_id}")
async def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    stmt = update(User).where(User.id == user_id).values(
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age
    )
    result = db.execute(stmt)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}

@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    stmt = delete(User).where(User.id == user_id)
    result = db.execute(stmt)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User deleted successfully!'}
