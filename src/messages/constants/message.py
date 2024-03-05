from django.db.models import TextChoices


class MessageType(TextChoices):
    MESSAGE = "message"


class MessageSubType(TextChoices):
    EMPTY = ""
    MESSAGE_CHANGED = "message_changed"
    MESSAGE_REPLIED = "message_replied"
    CHANNEL_JOINED = "channel_joined"
    BOT_MESSAGE = "bot_message"
