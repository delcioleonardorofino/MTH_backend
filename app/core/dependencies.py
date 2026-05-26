from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db
from ..models.user import User
from .config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

security = HTTPBearer()

async def get_current_user(db: AsyncSession = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get('sub')

        if not user_id:
            raise HTTPException(status_code=401, detail='Invalid Token!')

    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid Token!')
    
    result = await db.execute(select(User).where(User.id==user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401)
    
    return user

