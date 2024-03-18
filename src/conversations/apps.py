from django.apps import AppConfig
from conversations.queues import ConversationQueue


class ConversationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'conversations'

    def ready(self):
        ConversationQueue.declare_exchange()
