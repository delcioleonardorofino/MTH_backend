from fastapi import APIRouter, HTTPException, Depends
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from .services import fetch_all_users, fetch_user_by_id


router = APIRouter()

@router.get('/users')
async def get_users(db: AsyncSession = Depends(get_db)):
    
    return await fetch_all_users(db)

@router.get('/users/{user_id}')
async def get_user_by_id(user_id: str, db: AsyncSession = Depends(get_db)):

    user = await fetch_user_by_id(user_id, db)

    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found!")
    
    return user


    