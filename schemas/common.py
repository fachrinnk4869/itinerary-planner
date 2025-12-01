from pydantic import BaseModel, ConfigDict


class InternalServerErrorResponse(BaseModel):
    detail: str


class NotFoundResponse(BaseModel):
    detail: str = "Not found"
