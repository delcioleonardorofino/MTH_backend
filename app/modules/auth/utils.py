from fastapi import Request
from app.core.oauth import oauth
from app.models.user import User
from app.models.auth_account import OAuthAccount
from sqlalchemy.orm import Session


async def handle_redirect(request: Request):

    redirect_uri = request.url_for('github_callback')
    return await oauth.github.authorize_redirect(request, redirect_uri)

async def handle_user_login(request: Request, db: Session):
    provider = 'github'

    # Fazemos uma troca do code fornecido no redirect do github por access token 
    token = await oauth.github.authorize_access_token(request) 
    access_token = token['access_token']

    # Buscamos o user no github atraves do nosso token e retornamos as infos do user
    response = await oauth.github.get('user', token=token)
    user_info = response.json()

    # criamos variaveis com o id do provider, name do user e avatar_url
    provider_account_id = str(user_info['id'])
    name = user_info['login']
    avatar = user_info['avatar_url']

    # Verificar se OAuthAccount ja existe
    oauth_acount = db.query(OAuthAccount).filter_by(provider=provider, provider_account_id=provider_account_id).first()

    if oauth_acount:
        user = db.query(User).filter_by(id=oauth_acount.user_id).first()

    else:
        user = User(
            name=name,
            avatar_url=avatar
        )
        db.add(user)
        db.flush()

        oauth_acount = OAuthAccount(
            user_id=user.id,
            provider=provider,
            provider_account_id=provider_account_id,
            access_token=access_token
        )
        db.add(oauth_acount)
    
    db.commit()
    db.refresh(user)

    return {
        'id': str(user_info['id']),
        'name' : user_info['login'],
        'avatar' : user_info['avatar_url'],
    }
