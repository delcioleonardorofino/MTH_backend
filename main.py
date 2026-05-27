import os
from fastapi import FastAPI, Depends
from starlette.middleware.sessions import SessionMiddleware
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.projects.router import router as projects_router
from app.core.dependencies import get_current_user


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
app.include_router(
    projects_router
)


@app.get('/')
def health(current_user = Depends(get_current_user)):
    return {current_user}

@app.get('/test1')
def first_test():
    return 'Hello!'