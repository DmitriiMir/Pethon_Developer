from sqlalchemy.schema import CreateTable
from app_hw3.backend.db import Base, engine
from app_hw3.models.task import Task
from app_hw3.models.user import User

Base.metadata.create_all(engine)

print(CreateTable(Task.__table__))
print(CreateTable(User.__table__))
