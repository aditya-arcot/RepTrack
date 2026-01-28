from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database.access_request import AccessRequest
from app.models.schemas.access_request import AccessRequestPublic


async def get_access_requests(db: AsyncSession) -> list[AccessRequestPublic]:
    result = await db.execute(
        select(AccessRequest).order_by(AccessRequest.created_at.desc())
    )
    return [
        AccessRequestPublic.model_validate(ar, from_attributes=True)
        for ar in result.scalars().all()
    ]
