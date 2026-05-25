from authlib.integrations.starlette_client import OAuth
import os
from .config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET

oauth = OAuth()

oauth.register(
    name='github',
    client_id=GITHUB_CLIENT_ID,
    client_secret=GITHUB_CLIENT_SECRET,
    authorize_url='https://github.com/login/oauth/authorize',
    access_token_url='https://github.com/login/oauth/access_token',
    api_base_url='https://api.github.com/',
    client_kwargs={
        "scope":"read:user repo"
    }
)