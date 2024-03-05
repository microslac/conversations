from api.settings import env
from django.db import DEFAULT_DB_ALIAS

REPLICATION_DB_ALIAS = "replication"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Database
DATABASES = {
    DEFAULT_DB_ALIAS: {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    },
    REPLICATION_DB_ALIAS: {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "TEST": {
            "MIRROR": "default",
        },
    },
}
