from uuid import UUID

from fastapi import Request
from app.core.oauth import oauth
from app.models.user import User
from app.models.auth_account import OAuthAccount

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def handle_redirect(request: Request):
    redirect_uri = request.url_for("github_callback")
    return await oauth.github.authorize_redirect(request, redirect_uri)


async def handle_user_login(request: Request, db: AsyncSession):
    provider = "github"

    # 1. Trocar code por access token
    token = await oauth.github.authorize_access_token(request)
    access_token = token["access_token"]

    # 2. Buscar user no GitHub
    response = await oauth.github.get("user", token=token)
    user_info = response.json()

    provider_account_id = str(user_info["id"])
    name = user_info["login"]
    avatar = user_info["avatar_url"]

    # --------------------------------------------------
    # 3. Buscar OAuthAccount
    # --------------------------------------------------
    result = await db.execute(
        select(OAuthAccount).where(
            OAuthAccount.provider == provider,
            OAuthAccount.provider_account_id == provider_account_id
        )
    )

    oauth_account = result.scalar_one_or_none()

    # --------------------------------------------------
    # 4. Se já existe
    # --------------------------------------------------
    if oauth_account:
        result = await db.execute(
            select(User).where(User.id == oauth_account.user_id)
        )
        user = result.scalar_one_or_none()

    # --------------------------------------------------
    # 5. Se não existe → criar tudo
    # --------------------------------------------------
    else:
        user = User(
            name=name,
            avatar_url=avatar
        )

        db.add(user)
        await db.flush()  # garante user.id

        oauth_account = OAuthAccount(
            user_id=user.id,
            provider=provider,
            provider_account_id=provider_account_id,
            access_token=access_token
        )

        db.add(oauth_account)

    # --------------------------------------------------
    # 6. commit final
    # --------------------------------------------------
    await db.commit()
    await db.refresh(user)

    return {
        "id": str(user.id),
        "name": user.name,
        "avatar": user.avatar_url,
    }