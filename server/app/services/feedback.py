import logging
import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TypedDict

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.database.feedback import Feedback
from app.models.schemas.feedback import CreateFeedbackRequest
from app.models.schemas.user import UserPublic
from app.services.storage import store_files

logger = logging.getLogger(__name__)

FEEDBACK_DIR = settings.DATA_DIR / "feedback"


async def create_feedback(
    user: UserPublic,
    payload: CreateFeedbackRequest,
    db: AsyncSession,
):
    logger.info(f"Received feedback from user: {user.username}")

    stored_files = await store_files(payload.files, FEEDBACK_DIR)
    feedback = Feedback(
        user_id=user.id,
        type=payload.type,
        text=payload.text,
        files=stored_files,
    )

    db.add(feedback)
    await db.commit()
    await db.refresh(feedback)

    logger.info(f"Stored feedback from user: {user.username} with id: {feedback.id}")
