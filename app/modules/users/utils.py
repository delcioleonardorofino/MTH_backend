from fastapi import Request
from ...models.user import User
from sqlalchemy.orm import Session


def fetch_all_users(db:Session):

    users = db.query(User).all()

    return users

def fetch_user_by_id(user_id: str, db: Session):

    user = db.query(User).filter_by(id=user_id).first()

    return user