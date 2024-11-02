# uvicorn module_16_3:app --reload
from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()


users = {"1": "Имя: Example, возраст: 18"}

# GET запрос для получения всех пользователей
@app.get("/users")
async def get_users():
    return users

# POST запрос для добавления нового пользователя
@app.post("/user/{username}/{age}")
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
    new_user_id = str(max(map(int, users.keys())) + 1)
    users[new_user_id] = f"Имя: {username}, возраст: {age}"
    return {"message": f"User {new_user_id} is registered"}

# PUT запрос для обновления информации о пользователе
@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
    user_id: Annotated[
        str,
        Path(
            title="Enter User ID",
            description="ID пользователя",
            example="1"
        )
    ],
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
    if user_id in users:
        users[user_id] = f"Имя: {username}, возраст: {age}"
        return {"message": f"User {user_id} has been updated"}
    else:
        return {"error": "User not found"}

# DELETE запрос для удаления пользователя
@app.delete("/user/{user_id}")
async def delete_user(
    user_id: Annotated[
        str,
        Path(
            title="Enter User ID",
            description="ID пользователя",
            example="2"
        )
    ]
):
    if user_id in users:
        del users[user_id]
        return {"message": f"User {user_id} has been deleted"}
    else:
        return {"error": "User not found"}
