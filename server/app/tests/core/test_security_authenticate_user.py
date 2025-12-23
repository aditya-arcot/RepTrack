from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import authenticate_user


async def test_authenticate_user(session: AsyncSession):
    user = await authenticate_user(
        username=settings.ADMIN_USERNAME,
        password=settings.ADMIN_PASSWORD,
        db=session,
    )

    assert user is not None
    assert user.username == settings.ADMIN_USERNAME


async def test_authenticate_non_existent_user(session: AsyncSession):
    user = await authenticate_user(
        username="non_existent_user",
        password="some_password",
        db=session,
    )

    assert user is None


async def test_authenticate_user_invalid_password(session: AsyncSession):
    user = await authenticate_user(
        username=settings.ADMIN_USERNAME,
        password="some_password",
        db=session,
    )

    assert user is None
