from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .utils import handle_redirect, handle_user_login
from app.core.database import get_db

router = APIRouter()


@router.get("/login/github")
async def login_github(request: Request):
    return await handle_redirect(request=request)


@router.get("/auth/github/callback", name="github_callback")
async def github_callback(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    return await handle_user_login(
        provider="github",
        request=request,
        db=db
    )