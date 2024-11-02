# uvicorn module_16_4:app --reload
from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import List, Annotated

app = FastAPI()

# Список пользователей
users: List["User"] = []

# Модель пользователя
class User(BaseModel):
    id: int
    username: str
    age: int

# GET запрос для получения всех пользователей
@app.get("/users", response_model=List[User])
async def get_users():
    return users

# POST запрос для добавления нового пользователя
@app.post("/user/{username}/{age}", response_model=User)
async def add_user(
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
    # Определяем id нового пользователя
    new_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

# PUT запрос для обновления информации о пользователе
@app.put("/user/{user_id}/{username}/{age}", response_model=User)
async def update_user(
    user_id: Annotated[int, Path(title="Enter User ID", description="ID пользователя", example=1)],
    username: Annotated[
        str,
        Path(
            title="Enter username",
            description="Имя пользователя",
            min_length=5,
            max_length=20,
            example="UrbanProfi"
        )
    ],
    age: Annotated[
        int,
        Path(
            title="Enter age",
            description="Возраст пользователя",
            ge=18,
            le=120,
            example=28
        )
    ]
):
    # Поиск пользователя по user_id
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    # Если пользователь не найден, выбрасываем исключение
    raise HTTPException(status_code=404, detail="User was not found")

# DELETE запрос для удаления пользователя
@app.delete("/user/{user_id}", response_model=User)
async def delete_user(
    user_id: Annotated[int, Path(title="Enter User ID", description="ID пользователя", example=2)]
):
    # Поиск пользователя по user_id и удаление из списка
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    # Если пользователь не найден, выбрасываем исключение
    raise HTTPException(status_code=404, detail="User was not found")
