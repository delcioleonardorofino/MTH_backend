from fastapi import Request
from models.user import User
from sqlalchemy.orm import Session


async def fetch_all_users(db:Session):

    users = db.query(User).all()

    return users