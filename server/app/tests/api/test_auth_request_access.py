from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database.access_request import AccessRequest, AccessRequestStatus
from app.models.database.user import User
from app.models.errors import (
    AccessRequestPending,
    AccessRequestRejected,
    EmailAlreadyRegistered,
)


async def test_request_access(client: AsyncClient):
    resp = await client.post(
        "/api/auth/request-access",
        json={
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
        },
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "success"
    assert body["code"] == "ACCESS_REQUEST_CREATED"
    assert body["message"] == "Access request created. Please wait for admin approval."
    data = body["data"]
    assert "access_request_id" in data


async def test_request_access_approved(client: AsyncClient, session: AsyncSession):
    req = AccessRequest(
        email="approved@example.com",
        first_name="Approved",
        last_name="User",
        status=AccessRequestStatus.APPROVED,
    )
    session.add(req)
    await session.commit()

    resp = await client.post(
        "/api/auth/request-access",
        json={
            "email": "approved@example.com",
            "first_name": "Test",
            "last_name": "User",
        },
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "success"
    assert body["code"] == "ACCESS_REQUEST_ALREADY_APPROVED"
    assert body["message"] == "Access request already approved. Approval email resent."
    data = body["data"]
    assert "access_request_id" in data


async def test_request_access_existing_user(client: AsyncClient, session: AsyncSession):
    user = User(
        email="existing@example.com",
        username="existing",
        first_name="Existing",
        last_name="User",
        password_hash="hash",
        is_admin=False,
    )
    session.add(user)
    await session.commit()

    resp = await client.post(
        "/api/auth/request-access",
        json={
            "email": "existing@example.com",
            "first_name": "Test",
            "last_name": "User",
        },
    )

    assert resp.status_code == EmailAlreadyRegistered.http_status
    body = resp.json()
    assert body["status"] == "error"
    assert body["code"] == EmailAlreadyRegistered.code
    assert body["message"] == EmailAlreadyRegistered.message
    data = body["data"]
    assert data is None


async def test_request_access_pending(client: AsyncClient, session: AsyncSession):
    req = AccessRequest(
        email="pending@example.com",
        first_name="Pending",
        last_name="User",
        status=AccessRequestStatus.PENDING,
    )
    session.add(req)
    await session.commit()

    resp = await client.post(
        "/api/auth/request-access",
        json={
            "email": "pending@example.com",
            "first_name": "Test",
            "last_name": "User",
        },
    )

    assert resp.status_code == AccessRequestPending.http_status
    body = resp.json()
    assert body["status"] == "error"
    assert body["code"] == AccessRequestPending.code
    assert body["message"] == AccessRequestPending.message
    data = body["data"]
    assert data is None


async def test_request_access_rejected(client: AsyncClient, session: AsyncSession):
    req = AccessRequest(
        email="rejected@example.com",
        first_name="Rejected",
        last_name="User",
        status=AccessRequestStatus.REJECTED,
    )
    session.add(req)
    await session.commit()

    resp = await client.post(
        "/api/auth/request-access",
        json={
            "email": "rejected@example.com",
            "first_name": "Test",
            "last_name": "User",
        },
    )

    assert resp.status_code == AccessRequestRejected.http_status
    body = resp.json()
    assert body["status"] == "error"
    assert body["code"] == AccessRequestRejected.code
    assert body["message"] == AccessRequestRejected.message
    data = body["data"]
    assert data is None
