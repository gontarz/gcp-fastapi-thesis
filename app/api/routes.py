import io
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import JSONResponse, Response, StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies import basic_auth, get_current_user
from config import get_settings
from models.request import KMSKey, User, UserCreate
from services.auth import AuthError, authenticate_user, create_token, register_user
from services.firestore import update_user_kms_key
from services.kms import create_key_version, create_kms_key_for_user, validate_kms_key
from services.storage import delete_file, download_file, list_files, upload_file

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
def list_user_files(user: Annotated[User, Depends(get_current_user)]):
    return list_files(username=user.username)


@router.post("/files/upload")
def upload(file: UploadFile, user: Annotated[User, Depends(get_current_user)]):
    max_size = 5
    # max size of file limit
    if file.size > max_size * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"File size too large. Max size is {max_size} MB.")

    return upload_file(file=file, user=user)


@router.get("/files/{filename}")
def get_file(filename: str, user: Annotated[User, Depends(get_current_user)]) -> StreamingResponse:
    file_content = download_file(filename, user)
    return StreamingResponse(
        content=io.BytesIO(file_content),
        media_type="application/octet-stream"
    )


@router.delete("/files/{filename}")
def delete_user_file(filename: str, user: Annotated[User, Depends(get_current_user)]):
    delete_file(filename, user.username)
    return Response()


@router.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    logger.info(f"username {form_data.username} tries to obtain token")

    try:
        user = authenticate_user(form_data.username, form_data.password)
    except AuthError as err:
        raise HTTPException(status_code=401, detail=str(err))

    token = create_token(user=user)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", dependencies=[Depends(basic_auth)])
def register(user: UserCreate):
    try:
        created_user = register_user(username=user.username, password=user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "User registered successfully", "user_id": created_user.username}


@router.put("/kms/update")
def update_kms_key(key: KMSKey, user: Annotated[User, Depends(get_current_user)]):
    if not validate_kms_key(key.key):
        raise HTTPException(status_code=400, detail="Invalid or inaccessible KMS key")

    user.kms_key = key.key
    update_user_kms_key(username=user.username, kms_key=user.kms_key)

    return {"kms_key": user.kms_key}


@router.post("/kms/create")
def create_user_kms_key(user: Annotated[User, Depends(get_current_user)]):
    try:
        result = create_kms_key_for_user(key_id=f"key-{user.username}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"key_name": result}


@router.post("/kms/rotate")
def rotate_user_kms_key(user: Annotated[User, Depends(get_current_user)]):
    try:
        result = create_key_version(key_id=f"key-{user.username}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"key_name": result}
