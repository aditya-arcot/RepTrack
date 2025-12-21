from unittest.mock import AsyncMock

import pytest

from app.services.email import EmailService


@pytest.fixture
def mock_email_svc():
    service = AsyncMock(spec=EmailService)
    service.send_access_request_notification = AsyncMock()
    service.send_access_request_approved_email = AsyncMock()
    return service
