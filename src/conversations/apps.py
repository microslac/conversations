from django.apps import AppConfig
from django.conf import settings
from micro.events.registry import CommunicationEvents


class ConversationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "conversations"

    def ready(self):
        if settings.RABBITMQ_ENABLED:
            CommunicationEvents.declare_exchange()
