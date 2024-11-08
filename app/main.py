import uuid
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import get_db
from .logger import setup_logger
from .models import create_tables
from .schemas import CreatePayloadRequest, CreatePayloadResponse, GetPayloadResponse
from .service import (
    create_payload as create_payload_service,
    get_payload as get_payload_service,
    DifferentInputLengthError,
)


logger = setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/payload", response_model=CreatePayloadResponse)
async def create_payload(
    payload: CreatePayloadRequest, db: AsyncSession = Depends(get_db)
):
    try:
        result_id = await create_payload_service(payload.list_1, payload.list_2, db)
    except DifferentInputLengthError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.error(f"An error occurred: {exc}")
        raise HTTPException(status_code=500)
    return CreatePayloadResponse(id=result_id)


@app.get("/payload/{id}", response_model=GetPayloadResponse)
async def get_payload(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    try:
        payload = await get_payload_service(id, db)
    except Exception as exc:
        logger.error(f"An error occurred: {exc}")
        raise HTTPException(status_code=500)

    if payload is None:
        raise HTTPException(status_code=404, detail="Payload not found")
    return GetPayloadResponse(id=id, output=payload.output)
