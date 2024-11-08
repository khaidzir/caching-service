import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.models import create_tables
from app.schemas import CreatePayloadRequest, CreatePayloadResponse, GetPayloadResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/payload", response_model=CreatePayloadResponse)
def create_payload(payload: CreatePayloadRequest):
    return CreatePayloadResponse(id=uuid.uuid4())


@app.get("/payload/{id}", response_model=GetPayloadResponse)
def get_payload(id: uuid.UUID):
    return GetPayloadResponse(id=id, output="output")
