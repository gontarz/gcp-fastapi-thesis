import logging

from fastapi import HTTPException
from google.cloud import storage

from config import get_settings

settings = get_settings()
logger = logging.getLogger("uvicorn")
client = storage.Client()
bucket = client.bucket(settings.GCP_BUCKET_NAME)


def upload_file(file, user):
    blob = bucket.blob(f"{user.id}/{file.filename}")
    blob.kms_key_name = user.kms_key or settings.GCP_DEFAULT_KMS_KEY  # TODO
    # file.seek(0) # TODO
    try:
        blob.upload_from_file(file.file)
    except Exception as e:
        logger.exception(f"Failed to upload file '{file.filename}' for user '{user.id}': {e}")
        raise HTTPException(status_code=500, detail="Upload failed")

    return {"filename": file.filename, "message": "Uploaded successfully", "kms": blob.kms_key_name}


def list_files(user_id):
    blobs = bucket.list_blobs(prefix=f"{user_id}/")
    return [
        {"name": blob.name.split("/", 1)[-1], "kms_key": blob.kms_key_name}
        for blob in blobs if blob.name != f"{user_id}/"
    ]


def download_file(filename, user_id):
    blob = bucket.blob(f"{user_id}/{filename}")
    if not blob.exists():
        logger.error(f"File '{filename}' not found for user '{user_id}'")
        raise HTTPException(status_code=404, detail="File not found")
    return blob.download_as_bytes()


def delete_file(filename, user_id):
    blob = bucket.blob(f"{user_id}/{filename}")
    if not blob.exists():
        logger.error(f"File '{filename}' not found for user '{user_id}'")
        raise HTTPException(status_code=404, detail="File not found")
    blob.delete()
    return {"filename": filename, "message": "Deleted successfully"}
