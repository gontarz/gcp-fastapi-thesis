from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str
    password: str
    kms_key: str | None = None


class UserCreate(BaseModel):
    username: str
    password: str

class KMSKey(BaseModel):
    key:str
