from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_admin, get_db
from app.models.schemas.access_request import AccessRequestPublic
from app.models.schemas.errors import ErrorResponseModel
from app.models.schemas.user import UserPublic
from app.services.admin import get_access_requests, get_users

api_router = APIRouter(
    prefix="/admin", tags=["Admin"], dependencies=[Depends(get_current_admin)]
)


@api_router.get(
    "/access-requests",
    operation_id="getAccessRequests",
    responses={
        status.HTTP_401_UNAUTHORIZED: ErrorResponseModel,
        status.HTTP_403_FORBIDDEN: ErrorResponseModel,
    },
)
async def get_access_requests_endpoint(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[AccessRequestPublic]:
    return await get_access_requests(db)


@api_router.get(
    "/users",
    operation_id="getUsers",
    responses={
        status.HTTP_401_UNAUTHORIZED: ErrorResponseModel,
        status.HTTP_403_FORBIDDEN: ErrorResponseModel,
    },
)
async def get_users_endpoint(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[UserPublic]:
    return await get_users(db)
