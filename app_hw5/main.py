from fastapi import FastAPI
from app_hw5.routers import user
from app_hw5.routers import task

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(task.router, prefix="/task", tags=["task"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


