import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_create_payload():
    async with AsyncClient(transport=ASGITransport(app=app)) as client:
        response = await client.post(
            "http://test/payload",
            json={
                "list_1": ["first string", "second string", "third string"],
                "list_2": ["other string", "another string", "last string"],
            },
        )
        assert response.status_code == 200
        assert isinstance(response.json()["id"], str)
