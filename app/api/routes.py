import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from fastapi.responses import JSONResponse

from api.dependencies import get_current_user
from config import get_settings
from models.user import User, UserCreate
from services.auth import authenticate_user, load_users, register_user, save_user, validate_kms_key
from services.storage import delete_file, download_file, list_files, upload_file
from services.kms import create_kms_key_for_user, create_key_version

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()

settings = get_settings()


@router.get("/healthcheck")
async def healthcheck():
    return JSONResponse("OK")


@router.get("/")
async def root():
    return JSONResponse("OK")


@router.get("/files")
def list_user_files(user:User = Depends(get_current_user)):
    return list_files(user.id)


@router.post("/files/upload")
def upload(file: UploadFile = File(...), user:User = Depends(get_current_user)):
    return upload_file(file, user)


@router.get("/files/{filename}")
def get_file(filename: str, user:User = Depends(get_current_user)):
    return download_file(filename, user.id)


@router.delete("/files/{filename}")
def delete_user_file(filename: str, user:User = Depends(get_current_user)):
    return delete_file(filename, user.id)


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info(f"username {form_data.username} tries to obtain token")
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode = {"sub": user.id, "exp": expire}
    token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register")
def register(user: UserCreate):
    try:
        created_user = register_user(user.username, user.password)
        return {"message": "User registered successfully", "user_id": created_user.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.put("/kms-key")
def update_kms_key(new_key: str, user: User = Depends(get_current_user)):
    if not validate_kms_key(new_key):
        raise HTTPException(status_code=400, detail="Invalid or inaccessible KMS key")

    users = load_users()
    for u in users:
        if u.id == user.id:
            u.kms_key = new_key
            save_user(u, overwrite=True)
            return {"message": "KMS key updated", "kms_key": u.kms_key}
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/kms/create")
def create_user_kms_key(user: User = Depends(get_current_user)):
    result = create_kms_key_for_user(user.id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/kms/rotate")
def rotate_user_kms_key(user: User = Depends(get_current_user)):
    result = create_key_version(user.id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result