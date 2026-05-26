from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Request
from app.core.oauth import oauth
from app.models.user import User
from app.models.auth_account import OAuthAccount


async def handle_user_login(provider: str, request: Request, db: AsyncSession):

    # 1. Exchange code for token
    token = await oauth.create_client(provider).authorize_access_token(request)
    access_token = token["access_token"]

    # 2. Provider-specific user info
    oauth_client = oauth.create_client(provider)

    response = await oauth_client.get("user", token=token)
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
        raise ValueError("Unsupported provider")

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
        user = User(
            name=name,
            avatar_url=avatar
        )

        db.add(user)
        await db.flush()

        oauth_account = OAuthAccount(
            user_id=user.id,
            provider=provider,
            provider_account_id=provider_account_id,
            access_token=access_token
        )

        db.add(oauth_account)

    # 6. Commit
    await db.commit()
    await db.refresh(user)

    return {
        "id": str(user.id),
        "name": user.name,
        "avatar": user.avatar_url,
    }