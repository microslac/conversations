from logging.config import dictConfig
from api import settings

DEBUG = True

# LOGGING
verbose_log_format = "[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s"

LOGGING_CONFIG = None
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": verbose_log_format, "datefmt": "%d/%b/%Y %H:%M:%S"},
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "core": {
            "level": "DEBUG",
            "class": "logging.handlers.WatchedFileHandler",
            "filename": settings.LOGS_ROOT / "core.log",
            "formatter": "verbose",
        },
        "query": {
            "level": "INFO",
            "class": "logging.handlers.WatchedFileHandler",
            "filename": settings.LOGS_ROOT / "queries.log",
        },
    },
    "loggers": {
        "console": {
            "handlers": ["console"],
            "propagate": True,
            "level": "DEBUG",
        },
        "core": {
            "handlers": ["core"],
            "level": "DEBUG",
        },
        "django.server": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "django.db.backends": {
            "handlers": ["query"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

dictConfig(LOGGING)
