import logging
from typing import Optional

from google.cloud import firestore

from config import get_settings
from models.request import User

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

settings = get_settings()

# default database "(default)"
client = firestore.Client(project=settings.GCP_PROJECT_ID)
collection = client.collection(settings.GCP_FIRESTORE_COLLECTION_NAME)


def get_user(username: str) -> Optional[User]:
    doc = collection.document(username).get()
    if doc.exists:
        return User.model_validate(doc.to_dict())
    return None


def create_user(username: str, user_data: dict):
    collection.document(username).set(user_data)


def update_user_kms_key(username: str, kms_key: str):
    collection.document(username).update({
        "kms_key": kms_key
    })
