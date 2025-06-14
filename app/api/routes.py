import io
import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse, Response, StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from api.dependencies import get_current_user
from config import get_settings
from models.request import KMSKey, User, UserCreate
from services.auth import authenticate_user, register_user,create_token
from services.kms import create_key_version, create_kms_key_for_user, validate_kms_key
from services.storage import delete_file, download_file, list_files, upload_file
from services.user import find_user_by_name, save_user

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()

settings = get_settings()


# @router.get("/healthcheck")
# async def healthcheck() -> JSONResponse:
#     return JSONResponse({"status": "OK"})


@router.get("/")
async def root() -> JSONResponse:
    return JSONResponse({"status": "OK"})


@router.get("/files")
def list_user_files(user: User = Depends(get_current_user)):
    return list_files(user.id)


@router.post("/files/upload")
def upload(file: UploadFile = File(...), user: User = Depends(get_current_user)):
    return upload_file(file, user)


@router.get("/files/{filename}")
def get_file(filename: str, user: User = Depends(get_current_user)) -> StreamingResponse:
    file_content = download_file(filename, user)
    return StreamingResponse(
        content=io.BytesIO(file_content),
        media_type="application/octet-stream"
    )


@router.delete("/files/{filename}")
def delete_user_file(filename: str, user: User = Depends(get_current_user)):
    delete_file(filename, user.id)
    return Response()


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info(f"username {form_data.username} tries to obtain token")
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_token(user=user)

    return {"access_token": token, "token_type": "bearer"}


@router.post("/register")
def register(user: UserCreate):
    try:
        created_user = register_user(user.username, user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "User registered successfully", "user_id": created_user.id}


@router.put("/kms/update")
def update_kms_key(key: KMSKey, user: User = Depends(get_current_user)):
    if not validate_kms_key(key.key):
        raise HTTPException(status_code=400, detail="Invalid or inaccessible KMS key")

    user = find_user_by_name(username=user.username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.kms_key = key.key
    save_user(user, overwrite=True)

    return {"kms_key": user.kms_key}


@router.post("/kms/create")
def create_user_kms_key(user: User = Depends(get_current_user)):
    try:
        result = create_kms_key_for_user(key_id=f"key-{user.id}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"key_name": result}


@router.post("/kms/rotate")
def rotate_user_kms_key(user: User = Depends(get_current_user)):
    try:
        result = create_key_version(key_id=f"key-{user.id}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"key_name": result}
