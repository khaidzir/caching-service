import uuid

import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_get_payload_not_found():
    async with AsyncClient(app=app, base_url="http://test") as client:
        _id = uuid.uuid4()
        response = await client.get(f"/payload/{_id}")
        assert response.status_code == 404
