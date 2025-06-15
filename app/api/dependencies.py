from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer

from models.request import User
from services.auth import AuthError, get_user_from_token, verify_basic_auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
basic_auth_security = HTTPBasic()


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        return get_user_from_token(token)
    except AuthError as err:
        raise HTTPException(status_code=401, detail=str(err))


def basic_auth(
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth_security)],
):
    try:
        verify_basic_auth(username=credentials.username, password=credentials.password)
    except AuthError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(err),
            headers={"WWW-Authenticate": "Basic"},
        )
