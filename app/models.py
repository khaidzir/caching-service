import uuid

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID

from .database import Base, engine


class PayloadCache(Base):
    __tablename__ = "payload_caches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # We hashes the payload to store in the database,
    # because it will produce a unique and fixed length value.
    # Also it provides an efficient lookup operation.
    # We use SHA-256 hash to store in the database.
    hash = Column(String(64), unique=True, index=True, nullable=False)

    input_payload = Column(JSONB, nullable=False)
    output = Column(Text, nullable=False)

    def __repr__(self):
        return f"<PayloadCache(id={self.id}, hash={self.hash})>"


class TransformerCache(Base):
    __tablename__ = "transformer_caches"

    # We use SHA-256 hash to store the hash of the payload
    hash = Column(String(64), primary_key=True)
    string_input = Column(Text, nullable=False)
    result = Column(Text, nullable=False)

    def __repr__(self):
        return f"<TransformerCache(hash={self.hash})>"


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
