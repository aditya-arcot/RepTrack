import pytest

from app.core.config import settings
from app.services.email import get_email_service


@pytest.fixture
def override_email_backend(monkeypatch: pytest.MonkeyPatch):
    original_backend = settings.EMAIL_BACKEND

    def _override(backend: str):
        monkeypatch.setattr(settings, "EMAIL_BACKEND", backend)
        return get_email_service()

    yield _override

    monkeypatch.setattr(settings, "EMAIL_BACKEND", original_backend)
