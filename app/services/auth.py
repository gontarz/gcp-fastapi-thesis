import logging
import uuid
from typing import Optional
from datetime import datetime, timedelta,timezone
from config import get_settings
from jose import jwt

import bcrypt

from models.request import User
from services.user import find_user_by_name, is_username_taken, save_user

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def register_user(username: str, password: str) -> User:
    if is_username_taken(username):
        raise ValueError("Username already taken")

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User(id=str(uuid.uuid4()), username=username, password=hashed_password)
    print("register", user)  # TODO
    save_user(user=user)
    return user


def authenticate_user(username: str, password: str) -> Optional[User]:
    user = find_user_by_name(username=username)
    if user is None:
        return None

    if bcrypt.checkpw(password.encode(), user.password.encode()) is False:
        return None

    return user


def create_token(user:User) -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode = {"sub": user.id, "exp": expire}
    token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token