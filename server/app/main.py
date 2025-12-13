from fastapi import FastAPI

from .api.health import router as health_router
from .core.config import settings


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(health_router)
    return app


print("Settings:")
for key, val in settings.model_dump().items():
    print(key, val)
app = create_app()
