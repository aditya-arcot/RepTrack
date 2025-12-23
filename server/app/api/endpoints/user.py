from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.models.schemas.user import UserPublic

api_router = APIRouter()


@api_router.get("/users/current")
def get_current_user_route(
    user: Annotated[UserPublic, Depends(get_current_user)],
) -> UserPublic:
    return user
