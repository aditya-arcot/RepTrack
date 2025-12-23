from fastapi import status
from httpx import AsyncClient

from app.core.config import settings
from app.models.errors import InvalidCredentials
from app.models.schemas.auth import LoginResponse


async def make_request(client: AsyncClient, username: str, password: str):
    return await client.post(
        "/api/auth/login",
        data={
            "username": username,
            "password": password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )


async def test_login(client: AsyncClient):
    resp = await make_request(
        client, username=settings.ADMIN_USERNAME, password=settings.ADMIN_PASSWORD
    )

    assert resp.status_code == status.HTTP_200_OK
    body = resp.json()
    LoginResponse.model_validate(body)
    assert "access_token" in body
    assert body["token_type"] == "bearer"


async def test_login_non_existent_user(client: AsyncClient):
    resp = await make_request(
        client, username="non_existent_user", password="some_password"
    )

    assert resp.status_code == InvalidCredentials.status_code
    body = resp.json()
    assert body["detail"] == InvalidCredentials.detail


async def test_login_invalid_password(client: AsyncClient):
    resp = await make_request(
        client, username=settings.ADMIN_USERNAME, password="some_password"
    )

    assert resp.status_code == InvalidCredentials.status_code
    body = resp.json()
    assert body["detail"] == InvalidCredentials.detail
