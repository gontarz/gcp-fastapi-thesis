import logging

from fastapi import File, HTTPException
from google.cloud import storage
from models.request import User

from config import get_settings

settings = get_settings()
logger = logging.getLogger("uvicorn")
client = storage.Client()
bucket = client.bucket(settings.GCP_BUCKET_NAME)


def upload_file(file:File, user:User) -> dict:
    blob = bucket.blob(f"{user.id}/{file.filename}")
    if user.kms_key:
        blob.kms_key_name = user.kms_key
    try:
        blob.upload_from_file(file.file)
    except Exception as e:
        logger.exception(f"Failed to upload file '{file.filename}' for user '{user.id}': {e}")
        raise HTTPException(status_code=500, detail="Upload failed")

    return {"filename": file.filename, "kms": blob.kms_key_name}


def list_files(user_id:str) -> list[dict]:
    blobs = bucket.list_blobs(prefix=f"{user_id}/")
    return [
        {"name": blob.name.split("/", 1)[-1], "kms_key": blob.kms_key_name}
        for blob in blobs if blob.name != f"{user_id}/"
    ]


def download_file(filename:str, user:User) -> bytes:
    blob = bucket.blob(f"{user.id}/{filename}")
    if not blob.exists():
        logger.error(f"File '{filename}' not found for user '{user.id}'")
        raise HTTPException(status_code=404, detail="File not found")
    return blob.download_as_bytes()


def delete_file(filename:str, user_id:str):
    blob = bucket.blob(f"{user_id}/{filename}")
    if not blob.exists():
        logger.error(f"File '{filename}' not found for user '{user_id}'")
        raise HTTPException(status_code=404, detail="File not found")
    blob.delete()
