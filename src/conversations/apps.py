from django.apps import AppConfig
from django.conf import settings


class ConversationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "conversations"

    def ready(self):
        if settings.RABBITMQ_ENABLED:
            from conversations.events import communication  # noqa
            from micro.events.publishers import registry

            registry.communication.declare_exchange()
