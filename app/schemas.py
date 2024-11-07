import uuid

from pydantic import BaseModel


class CreatePayloadRequest(BaseModel):
    list_1: list[str]
    list_2: list[str]


class CreatePayloadResponse(BaseModel):
    id: uuid.UUID


class GetPayloadResponse(BaseModel):
    id: uuid.UUID
    output: str
