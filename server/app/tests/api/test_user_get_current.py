from httpx import AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.database.user import User
from app.models.errors import InvalidCredentials
from app.models.schemas.user import UserPublic


async def login_and_get_token(client: AsyncClient):
    resp = await client.post(
        "/api/auth/login",
        data={
            "username": settings.ADMIN_USERNAME,
            "password": settings.ADMIN_PASSWORD,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    body = resp.json()
    return body["access_token"]


async def make_request(client: AsyncClient, token: str | None = None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return await client.get("/api/users/current", headers=headers)


async def test_get_current_user(client: AsyncClient):
    token = await login_and_get_token(client)
    resp = await make_request(client, token=token)

    assert resp.status_code == 200
    body = resp.json()
    UserPublic.model_validate(body)
    assert body["username"] == settings.ADMIN_USERNAME
    assert body["email"] == settings.ADMIN_EMAIL
    assert body["is_admin"] is True


async def test_get_current_user_no_token(client: AsyncClient):
    resp = await make_request(client)

    assert resp.status_code == 401
    body = resp.json()
    assert body["detail"] == "Not authenticated"


async def test_get_current_user_invalid_token(client: AsyncClient):
    resp = await make_request(client, token="invalid_token")

    assert resp.status_code == InvalidCredentials.status_code
    body = resp.json()
    assert body["detail"] == InvalidCredentials.detail


async def test_get_current_user_deleted_user(
    client: AsyncClient, session: AsyncSession
):
    token = await login_and_get_token(client)

    await session.execute(delete(User).where(User.username == settings.ADMIN_USERNAME))
    await session.commit()

    resp = await make_request(client, token=token)

    assert resp.status_code == InvalidCredentials.status_code
    body = resp.json()
    assert body["detail"] == InvalidCredentials.detail
