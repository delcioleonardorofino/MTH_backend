from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from core.oauth import oauth
from core.database import get_db 
from models.user import User
from models.auth_account import OAuthAccount

router = APIRouter()

# Endpoint por onde o user comeca o fluxo de login
@router.get('/login/github')
async def login_github(request: Request):
    
    redirect_uri = request.url_for('github_callback')

    print(redirect_uri)

    return await oauth.github.authorize_redirect(request, redirect_uri)

# Depois de acessar /login/github o user sera redirected para a seguinte url tal como definido em redirect_uri = request.url_for('github_callback'). o github_callback deve ser o nome do endpoint abaixo.

@router.get('/auth/github/callback', name='github_callback')
async def github_callback(request: Request, db = Depends(get_db)):
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
