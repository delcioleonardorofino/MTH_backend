from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import handle_user_login
from app.core.database import get_db
from app.core.oauth import SUPPORTED_PROVIDERS, oauth

router = APIRouter()


@router.get("/login/{provider}")
async def login_w_provider(provider: str, request: Request):

    if provider not in SUPPORTED_PROVIDERS:
        raise HTTPException(status_code=400, detail="Unsupported provider")

    client = oauth.create_client(provider)

    redirect_uri = request.url_for("callback_function", provider=provider)

    return await client.authorize_redirect(request, redirect_uri)


@router.get("/auth/{provider}/callback", name="callback_function")
async def callback_endpoint(
    provider: str,
    request: Request,
    db: AsyncSession = Depends(get_db)
):

    if provider not in SUPPORTED_PROVIDERS:
        raise HTTPException(status_code=400, detail="Unsupported provider")
    
    return await handle_user_login(
        provider=provider,
        request=request,
        db=db
    )