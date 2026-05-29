import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.projects.router import router as projects_router
from app.core.dependencies import get_current_user
from app.core.config import settings

ALLOWED_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000', 'https://mthub.vercel.app']

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

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
app.include_router(
    projects_router
)


@app.get('/')
def health():
    return {"Message": 'Hello, User!'}

@app.get('/test1')
def first_test():
    return 'Hello!'

