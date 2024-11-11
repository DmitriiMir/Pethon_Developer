from fastapi import FastAPI
from app.routers.task import router as task_router
from app.routers.user import router as user_router



# Создаём объект приложения
app = FastAPI()

# Основной маршрут
@app.get("/")
async def root():
    return {"message": "Welcome to Taskmanager"}

# Подключение маршрутов
app.include_router(task_router)
app.include_router(user_router)

