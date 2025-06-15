import logging

from fastapi import File, HTTPException
from google.cloud import storage

from config import get_settings
from models.request import User

settings = get_settings()
logger = logging.getLogger("uvicorn")
client = storage.Client()
bucket = client.bucket(settings.GCP_BUCKET_NAME)


def upload_file(file: File, user: User) -> dict:
    blob = bucket.blob(f"{user.username}/{file.filename}")
    if user.kms_key:
        blob.kms_key_name = user.kms_key
    try:
        blob.upload_from_file(file.file)
    except Exception as e:
        logger.exception(f"Failed to upload file '{file.filename}' for user '{user.username}': {e}")
        raise HTTPException(status_code=500, detail="Upload failed")

    return {"filename": file.filename, "kms": blob.kms_key_name}


def list_files(username: str) -> list[dict]:
    blobs = bucket.list_blobs(prefix=f"{username}/")
    return [
        {"name": blob.name.split("/", 1)[-1], "kms_key": blob.kms_key_name}
        for blob in blobs if blob.name != f"{username}/"
    ]


def download_file(filename: str, user: User) -> bytes:
    blob = bucket.blob(f"{user.username}/{filename}")
    if not blob.exists():
        logger.error(f"File '{filename}' not found for user '{user.username}'")
        raise HTTPException(status_code=404, detail="File not found")
    return blob.download_as_bytes()


def delete_file(filename: str, username: str):
    blob = bucket.blob(f"{username}/{filename}")
    if not blob.exists():
        logger.error(f"File '{filename}' not found for user '{username}'")
        raise HTTPException(status_code=404, detail="File not found")
    blob.delete()
