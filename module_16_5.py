# uvicorn module_16_5:app --reload
from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Annotated

app = FastAPI()

# Инициализация Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Список пользователей
users: List["User"] = []

class User(BaseModel):
    id: int
    username: str
    age: int

# GET запрос для отображения списка всех пользователей на главной странице
@app.get("/", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

# GET запрос для получения информации о конкретном пользователе
@app.get("/user/{user_id}", response_class=HTMLResponse)
async def get_user(request: Request, user_id: int):
    # Поиск пользователя по user_id
    user = next((u for u in users if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User was not found")
    return templates.TemplateResponse("users.html", {"request": request, "user": user})

# POST запрос для добавления нового пользователя
@app.post("/user/{username}/{age}", response_model=User)
async def add_user(
    username: Annotated[
        str,
        Path(
            title="Enter username",
            description="Имя пользователя",
            min_length=5,
            max_length=20
        )
    ],
    age: Annotated[
        int,
        Path(
            title="Enter age",
            description="Возраст пользователя",
            ge=18,
            le=120
        )
    ]
):
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
            max_length=20
        )
    ],
    age: Annotated[
        int,
        Path(
            title="Enter age",
            description="Возраст пользователя",
            ge=18,
            le=120
        )
    ]
):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")

# DELETE запрос для удаления пользователя
@app.delete("/user/{user_id}", response_model=User)
async def delete_user(
    user_id: Annotated[int, Path(title="Enter User ID", description="ID пользователя", example=2)]
):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")
