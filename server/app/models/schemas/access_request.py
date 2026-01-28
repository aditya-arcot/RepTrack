from datetime import datetime

from pydantic import BaseModel

from app.models.enums import AccessRequestStatus


class AccessRequestPublic(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    status: AccessRequestStatus
    reviewed_at: datetime | None
    reviewed_by: int | None
    created_at: datetime
    updated_at: datetime
