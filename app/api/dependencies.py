from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from models.request import User
from services.auth import AuthError, get_user_from_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        return get_user_from_token(token)
    except AuthError as err:
        raise HTTPException(status_code=401, detail=str(err))
