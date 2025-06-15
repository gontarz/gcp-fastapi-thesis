from pydantic import BaseModel


class BaseResponse(BaseModel):
    msg: str | None = None
