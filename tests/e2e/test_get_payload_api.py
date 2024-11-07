import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_get_payload():
    async with AsyncClient(transport=ASGITransport(app=app)) as client:
        _id = uuid.uuid4()
        response = await client.get(f"http://test/payload/{_id}")
        assert response.status_code == 200
        assert isinstance(response.json()["id"], str)
        assert response.json()["id"] == str(_id)
        assert isinstance(response.json()["output"], str)
