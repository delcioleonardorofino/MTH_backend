import os
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from modules.auth.router import router as auth_router


app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv('SECRET_KEY')
)

app.include_router(
    auth_router
)

@app.get('/')
def health():
    return {"message": 'alive'}

for route in app.routes:
    print(route.path, route.name)