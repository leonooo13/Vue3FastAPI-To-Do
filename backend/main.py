from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import authentication, task, user


app = FastAPI()

app.include_router(user.router)
app.include_router(task.router)
app.include_router(authentication.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
