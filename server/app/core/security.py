from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.database.user import User

password_hash = PasswordHash.recommended()


async def authenticate_user(
    username: str,
    password: str,
    db: AsyncSession,
) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if not user or not password_hash.verify(password, user.password_hash):
        return None
    return user


def create_access_token(data: dict[str, Any]) -> str:
    data_copy = data.copy()
    delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data_copy["exp"] = datetime.now(timezone.utc) + delta
    token = jwt.encode(data_copy, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return str(token)
