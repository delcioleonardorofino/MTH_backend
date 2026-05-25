from fastapi import APIRouter, HTTPException, Depends
from app.core.database import get_db
from sqlalchemy.orm import Session
from .utils import fetch_all_users, fetch_user_by_id


router = APIRouter()

@router.get('/users')
def get_users(db: Session = Depends(get_db)):
    
    return fetch_all_users(db)

@router.get('/users/{user_id}')
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):

    user = fetch_user_by_id(user_id, db)

    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found!")
    
    return user


    