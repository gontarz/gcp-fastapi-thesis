import logging
import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from config import get_settings
from models.request import User
from services.firestore import create_user, get_user

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

settings = get_settings()


class AuthError(Exception):
    pass


def create_token(user: User) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode = {"sub": user.username, "exp": expire}
    token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token


def get_user_from_token(token: str) -> User:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        raise AuthError("Could not validate token")

    username: str = payload.get("sub")
    if username is None:
        raise AuthError("Invalid token")

    user = get_user(username=username)
    if user is None:
        raise AuthError("User not found")

    return user


def register_user(username: str, password: str) -> User:
    if get_user(username):
        raise AuthError("Username already taken")

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User(id=str(uuid.uuid4()), username=username, password=hashed_password)
    create_user(username=user.username, user_data=user.model_dump())
    logger.info(f"registered {user}")
    return user


def authenticate_user(username: str, password: str) -> User:
    user = get_user(username=username)
    if user is None:
        raise AuthError("User not found")

    if bcrypt.checkpw(password.encode(), user.password.encode()) is False:
        raise AuthError("Password check failed")

    return user
