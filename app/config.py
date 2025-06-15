from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    GCP_BUCKET_NAME:str
    GCP_DEFAULT_KMS_KEY:str
    GCP_FIRESTORE_COLLECTION_NAME: str = "users"
    GCP_KEY_RING_ID:str
    GCP_PROJECT_ID:str
    GCP_REGION:str

    JWT_ALGORITHM:str = "HS256"
    JWT_EXPIRE_MINUTES:int = 30
    JWT_SECRET_KEY:str

    BASIC_AUTH_USERNAME:str
    BASIC_AUTH_PASSWORD:str



@lru_cache
def get_settings() -> Settings:
    return Settings()
