import logging
import logging.config

from pythonjsonlogger.json import JsonFormatter

from app.core.config import settings


def setup_logging() -> None:
    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    }

    log_file = settings.LOG_DIR / f"reptrack_server_{settings.ENV}.log"
    handlers["file"] = {
        "class": "logging.FileHandler",
        "formatter": "json",
        "filename": str(log_file),
        "encoding": "utf-8",
    }

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "()": JsonFormatter,
                    "fmt": ("%(asctime)s %(levelname)s %(name)s %(message)s"),
                    "rename_fields": {
                        "asctime": "time",
                        "levelname": "level",
                        "name": "logger",
                    },
                },
            },
            "handlers": handlers,
            "root": {
                "level": settings.LOG_LEVEL,
                "handlers": list(handlers.keys()),
            },
        }
    )
