from jose import jwt
from datetime import datetime, timedelta
from .config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM


def create_access_token(data: dict):

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        'exp': expire
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

