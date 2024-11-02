from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

# Маршрут к главной странице
@app.get("/")
async def main_page():
    return {"message": "Главная страница"}

# Маршрут к странице администратора
@app.get("/user/admin")
async def admin_page():
    return {"message": "Вы вошли как администратор"}

# Маршрут к странице пользователя с параметром user_id и валидацией
@app.get("/user/{user_id}")
async def user_page(
    user_id: Annotated[
        int,
        Path(
            title="Enter User ID",
            description="ID пользователя",
            ge=1,
            le=100,
            example=1
        )
    ]
):
    return {"message": f"Вы вошли как пользователь № {user_id}"}

# Маршрут с информацией о пользователе
@app.get("/user/{username}/{age}")
async def user_info(
    username: Annotated[
        str,
        Path(
            title="Enter username",
            description="Имя пользователя",
            min_length=5,
            max_length=20,
            example="UrbanUser"
        )
    ],
    age: Annotated[
        int,
        Path(
            title="Enter age",
            description="Возраст пользователя",
            ge=18,
            le=120,
            example=24
        )
    ]
):
    return {"message": f"Информация о пользователе. Имя: {username}, Возраст: {age}"}
