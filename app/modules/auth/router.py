from fastapi import APIRouter, Request, Depends
from .utils import handle_redirect, handle_user_login
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# Endpoint por onde o user comeca o fluxo de login
@router.get('/login/github')
async def login_github(request: Request):
    return await handle_redirect(request=request)
    

# Depois de acessar /login/github o user sera redirected para a seguinte url tal como definido em redirect_uri = request.url_for('github_callback'). o github_callback deve ser o nome do endpoint abaixo.

@router.get('/auth/github/callback', name='github_callback')
async def github_callback(request: Request, db : Session = Depends(get_db)):
    return await handle_user_login(request=request, db=db)