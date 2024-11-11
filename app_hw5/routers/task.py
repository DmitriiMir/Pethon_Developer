from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app_hw5.backend.db_depends import get_db
from app_hw5.models.task import Task
from app_hw5.models.user import User
from app_hw5.schemas import CreateTask, UpdateTask
from typing import Annotated
from sqlalchemy import insert, select, update, delete




router = APIRouter()

@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks

@router.get("/{task_id}")
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=404, detail="Task was not found")
    return task

@router.post("/create")
async def create_task(task: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    new_task = Task(**task.dict(), user_id=user_id)
    db.add(new_task)
    db.commit()
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}

@router.put("/update")
async def update_task(task_id: int, task: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    db_task = db.scalar(select(Task).where(Task.id == task_id))
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task was not found")
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "Task update is successful!"}

@router.delete("/delete")
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=404, detail="Task was not found")
    db.delete(task)
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "Task deletion is successful!"}
