import os
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router


app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv('SECRET_KEY')
)

app.include_router(
    auth_router
)

app.include_router(
    users_router
)

@app.get('/')
def health():
    return {"message": 'alive'}

