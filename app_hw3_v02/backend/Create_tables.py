from sqlalchemy.schema import CreateTable
from backend.db import Base, engine
from models.task import Task
from models.user import User

Base.metadata.create_all(engine)

print(CreateTable(Task.__table__))
print(CreateTable(User.__table__))
