import json
import logging
from pathlib import Path
from typing import Optional

from models.request import User

USERS_FILE = Path("users.json")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

## TODO
if not USERS_FILE.exists():
    USERS_FILE.touch()
    with open(USERS_FILE, "w") as f:
        json.dump([], f, indent=2)
##

def load_users() -> list[User]:
    with open(USERS_FILE, "r") as f:
        data = json.load(f)
    return [User(**user) for user in data]


def find_user_by_name(username: str) -> Optional[User]:
    users = (u for u in load_users() if u.username == username)
    return next(users, None)


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
