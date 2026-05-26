from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import handle_user_login
from app.core.database import get_db
from app.core.oauth import SUPPORTED_PROVIDERS, oauth
from app.core.dependencies import get_current_user
from models.auth_account import OAuthAccount

router = APIRouter(prefix='/auth')


@router.get("/login/{provider}")
async def login_w_provider(provider: str, request: Request):

    if provider not in SUPPORTED_PROVIDERS:
        raise HTTPException(status_code=400, detail="Unsupported provider")

    client = oauth.create_client(provider)

    redirect_uri = request.url_for("oauth_callback_function", provider=provider)

    return await client.authorize_redirect(request, redirect_uri)


@router.get("/{provider}/callback", name="oauth_callback_function")
async def oauth_callback_endpoint(
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

# @router.get('/connect/{provider}')
# async def connect_provider(
#     provider: str,
#     request: Request
# ):

#     client = oauth.create_client(provider)

#     redirect_uri = request.url_for(
#         'connect_callback',
#         provider=property
#     )

#     return await client.authorize_redirect(request, redirect_uri)

# @router.get('/connect/{provider}/callback')
# async def connect_callback(
#     provider: str,
#     request: Request,
#     db: AsyncSession = Depends(get_db),
#     current_user = Depends(get_current_user)
# ):
#     request.session['link_user_id'] = str(current_user.id)
#     user_id = request.session.get('link_user_id')

#     if not user_id:
#         raise HTTPException(status_code=401)
    
#     client = oauth.create_client(provider)

#     token = await client.authorize_access_token(request)

#     if provider == 'google':
#         response = await client.get(
#             "https://openidconnect.googleapis.com/v1/userinfo",
#             token=token
#         )
#     else:
#         response = await client.get('user', token=token)

#     data = response.json()

#     oauth_account = OAuthAccount(
#         user_id = user_id,
#         provider = provider,
#         provider_account_id = str(data['id']),
#         access_token = token.get('access_token')
#     )

#     res = await db.execute(
#         select(OAuthAccount).where(
#             OAuthAccount.provider == provider,
#             OAuthAccount.provider_account_id == str(data['id'])
#         ))
    
#     existing = res.scalar_one_or_none()

#     if existing:
#         raise HTTPException(400, detail='Account already linked!')
    
#     db.add(oauth_account)

#     await db.commit()