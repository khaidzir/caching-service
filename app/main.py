import uuid

from fastapi import FastAPI

from app.schemas import CreatePayloadRequest, CreatePayloadResponse, GetPayloadResponse

app = FastAPI()


@app.post("/payload", response_model=CreatePayloadResponse)
def create_payload(payload: CreatePayloadRequest):
    return CreatePayloadResponse(id=uuid.uuid4())


@app.get("/payload/{id}", response_model=GetPayloadResponse)
def get_payload(id: uuid.UUID):
    return GetPayloadResponse(id=id, output="output")
