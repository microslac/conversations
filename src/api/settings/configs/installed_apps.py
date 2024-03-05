# Application definition
DJANGO_APPS = (
    # "django.contrib.admin",
    # "django.contrib.messages",
    # "django.contrib.sessions",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
)

THIRD_PARTY_APPS = (
    "corsheaders",
    "rest_framework",
)

APP_CHANNELS = "channels"
APP_MESSAGES = "messages"
APP_CONVERSATIONS = "conversations"

LOCAL_APPS = (APP_CHANNELS, APP_MESSAGES, APP_CONVERSATIONS)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
