from api.settings import env
from django.db import DEFAULT_DB_ALIAS

DEBUG = True

PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

# Database
REPLICATION_DB_ALIAS = "replication"
DATABASES = {
    DEFAULT_DB_ALIAS: {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_TEST_NAME"),
        "USER": env("DB_TEST_USER"),
        "PASSWORD": env("DB_TEST_PASSWORD"),
        "HOST": env("DB_TEST_HOST"),
        "PORT": env("DB_TEST_PORT"),
    },
    REPLICATION_DB_ALIAS: {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_TEST_NAME"),
        "USER": env("DB_TEST_USER"),
        "PASSWORD": env("DB_TEST_PASSWORD"),
        "HOST": env("DB_TEST_HOST"),
        "PORT": env("DB_TEST_PORT"),
        "TEST": {
            "MIRROR": "default",
        },
    },
}

# Logging
LOGGING = {}

ACCESS_TOKEN = env.str(
    "TEST_ACCESS_TOKEN",
    default="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzd3QiOiJhY2Nlc3MiLCJleHAiOjE3MDg2Njk1MzMsImlhdCI6MTcwODY2NTkzMywianRpIjoiMjRhNTE5NjNkYjlkNDc5MWJkNTY1NWJjYmVhZGNkODIiLCJhaWQiOiJBMDEyMzQ1Njc4OSIsInRpZCI6IlQwMTIzNDU2Nzg5IiwidWlkIjoiVTAxMjM0NTY3ODkifQ.cnuAEmGYPh8F-BT-S9rI-uqHftO50IjUcX55REpJW1gcQNvf2ZdGq2rOilGUxct8s6Ay6d9ySLtjW0z9VV71itYxFMjMfpnB1hwMhgOMBbipRQiD8BCC1-MehjfORPA2hPKc0-V8-GuxzE3uQh4pHw6IJs0C8_TqYT8P84F6bTIthoGRA0XRZQelXPGrhws5gn7vU9skrOJIdjSfSrSnWvn2zfPOCdEqshUy8imWd6ZWKtd2fWBzohObe3h0JdNHeT9amT5xul85hqahlS82kaYfHiKgJ95dkCTVzMcfiil9Wi4evw5sxteCE24dzmOdDqR2PyWzOWL0H_JlQKf7Gw"
)
