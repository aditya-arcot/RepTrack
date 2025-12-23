from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database.access_request import AccessRequest, AccessRequestStatus
from app.models.database.user import User
from app.models.errors import (
    AccessRequestPending,
    AccessRequestRejected,
    EmailAlreadyRegistered,
)
from app.models.schemas.auth import RequestAccessResponse


async def make_request(
    client: AsyncClient, email: str, first_name: str, last_name: str
):
    return await client.post(
        "/api/auth/request-access",
        json={
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
        },
    )


async def test_request_access(client: AsyncClient):
    resp = await make_request(
        client, email="new_user@example.com", first_name="New", last_name="User"
    )

    assert resp.status_code == status.HTTP_200_OK
    body = resp.json()
    RequestAccessResponse.model_validate(body)
    assert body["detail"] == "Access request created. Please wait for admin approval."
    assert body["access_request_id"] is not None


async def test_request_access_approved(client: AsyncClient, session: AsyncSession):
    approved_email = "approved@example.com"
    req = AccessRequest(
        email=approved_email,
        first_name="Approved",
        last_name="User",
        status=AccessRequestStatus.APPROVED,
    )
    session.add(req)
    await session.commit()

    resp = await make_request(
        client, email=approved_email, first_name="Test", last_name="User"
    )

    assert resp.status_code == status.HTTP_200_OK
    body = resp.json()
    RequestAccessResponse.model_validate(body)
    assert body["detail"] == "Access request already approved. Approval email resent."
    assert body["access_request_id"] is not None


async def test_request_access_existing_user(client: AsyncClient, session: AsyncSession):
    existing_email = "existing@example.com"
    user = User(
        email=existing_email,
        username="existing",
        first_name="Existing",
        last_name="User",
        password_hash="hash",
        is_admin=False,
    )
    session.add(user)
    await session.commit()

    resp = await make_request(
        client, email=existing_email, first_name="Test", last_name="User"
    )

    assert resp.status_code == EmailAlreadyRegistered.status_code
    body = resp.json()
    assert body["detail"] == EmailAlreadyRegistered.detail


async def test_request_access_pending(client: AsyncClient, session: AsyncSession):
    pending_email = "pending@example.com"
    req = AccessRequest(
        email=pending_email,
        first_name="Pending",
        last_name="User",
        status=AccessRequestStatus.PENDING,
    )
    session.add(req)
    await session.commit()

    resp = await make_request(
        client, email=pending_email, first_name="Test", last_name="User"
    )

    assert resp.status_code == AccessRequestPending.status_code
    body = resp.json()
    assert body["detail"] == AccessRequestPending.detail


async def test_request_access_rejected(client: AsyncClient, session: AsyncSession):
    rejected_email = "rejected@example.com"
    req = AccessRequest(
        email=rejected_email,
        first_name="Rejected",
        last_name="User",
        status=AccessRequestStatus.REJECTED,
    )
    session.add(req)
    await session.commit()

    resp = await make_request(
        client, email=rejected_email, first_name="Test", last_name="User"
    )

    assert resp.status_code == AccessRequestRejected.status_code
    body = resp.json()
    assert body["detail"] == AccessRequestRejected.detail
