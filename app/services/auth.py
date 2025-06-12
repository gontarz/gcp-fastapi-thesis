import json
import logging
import uuid
from pathlib import Path
from typing import Optional

import bcrypt
from google.cloud import kms

from models.user import User
from pathlib import Path

USERS_FILE = Path("users.json")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

## TODO
filename = Path(USERS_FILE)
filename.touch(exist_ok=True)  # will create file, if it exists will do nothing
##

def load_users() -> list[User]:
    with open(USERS_FILE, "r") as f:
        data = json.load(f)
    return [User(**user) for user in data]


def save_user(user: User, overwrite=False) -> None:
    users = load_users()
    if overwrite:
        users = [u for u in users if u.id != user.id]
    users.append(user)
    with open(USERS_FILE, "w") as f:
        json.dump([u.model_dump() for u in users], f, indent=2)


def is_username_taken(username: str) -> bool:
    logger.debug(f"username {username}")
    return any(u.username == username for u in load_users())


def register_user(username: str, password: str) -> User:
    if is_username_taken(username):
        raise ValueError("Username already taken")
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User(id=str(uuid.uuid4()), username=username, password=hashed_password)
    print("register", user) # TODO
    save_user(user)
    return user


def authenticate_user(username: str, password: str) -> Optional[User]:
    users = load_users()
    for user in users:
        if user.username == username and bcrypt.checkpw(password.encode(), user.password.encode()):
            return user
    return None


def validate_kms_key(key_name: str) -> bool:
    try:
        client = kms.KeyManagementServiceClient()
        client.get_crypto_key(request={"name": key_name})
        return True
    except Exception:
        return False
