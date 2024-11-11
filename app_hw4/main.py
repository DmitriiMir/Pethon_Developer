from fastapi import FastAPI
from app_hw4.routers import user

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


