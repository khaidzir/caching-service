import pytest

from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_create_payload_returning_the_same_id():
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "list_1": ["first string", "second string", "third string"],
            "list_2": ["other string", "another string", "last string"],
        }
        response = await client.post(
            "/payload",
            json=payload,
        )
        old_id = response.json()["id"]

        response = await client.post(
            "/payload",
            json=payload,
        )
        new_id = response.json()["id"]

        assert old_id == new_id
