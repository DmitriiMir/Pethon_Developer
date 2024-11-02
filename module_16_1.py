from fastapi import FastAPI
from typing import Optional

app = FastAPI()

# Маршрут к главной странице
@app.get("/")
async def main_page():
    return {"message": "Главная страница"}

# Маршрут к странице администратора
@app.get("/user/admin")
async def admin_page():
    return {"message": "Вы вошли как администратор"}

# Маршрут к странице пользователя
@app.get("/user/{user_id}")
async def user_page(user_id: int):
    return {"message": f"Вы вошли как пользователь № {user_id}"}

# Маршрут с передачей данных
@app.get("/user")
async def user_info(username: Optional[str] = "неизвестный", age: Optional[int] = 0):
    return {"message": f"Информация о пользователе. Имя: {username}, Возраст: {age}"}

