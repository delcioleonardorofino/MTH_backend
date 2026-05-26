from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Request, HTTPException
from app.core.oauth import oauth
from app.models.user import User
from app.models.auth_account import OAuthAccount


async def handle_user_login(provider: str, request: Request, db: AsyncSession):

    client = oauth.create_client(provider)

    # 1. Exchange code for token
    token = await client.authorize_access_token(request)
    access_token = token.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="Invalid token response")

    # 2. Fetch user info (provider-specific)
    if provider == "google":
        response = await client.get(
            "https://openidconnect.googleapis.com/v1/userinfo",
            token=token
        )
    else:
        response = await client.get("user", token=token)

    user_info = response.json()

    if provider == "github":
        provider_account_id = str(user_info["id"])
        name = user_info["login"]
        avatar = user_info["avatar_url"]

    elif provider == "google":
        provider_account_id = user_info["sub"]
        name = user_info.get("name")
        avatar = user_info.get("picture")

    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")

    # 3. Find OAuth account
    result = await db.execute(
        select(OAuthAccount).where(
            OAuthAccount.provider == provider,
            OAuthAccount.provider_account_id == provider_account_id
        )
    )

    oauth_account = result.scalar_one_or_none()

    # 4. Existing user
    if oauth_account:
        user = await db.get(User, oauth_account.user_id)

    # 5. Create new user
    else:
        user = User(name=name, avatar_url=avatar)
        db.add(user)
        await db.flush()

        db.add(OAuthAccount(
            user_id=user.id,
            provider=provider,
            provider_account_id=provider_account_id,
            access_token=access_token
        ))

    # 6. Commit
    await db.commit()
    await db.refresh(user)

    return {
        "id": str(user.id),
        "name": user.name,
        "avatar": user.avatar_url,
    }