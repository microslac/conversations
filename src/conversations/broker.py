from django.conf import settings
from faststream.rabbit import RabbitBroker

broker = RabbitBroker(
    host=settings.RABBITMQ_HOST,
    port=settings.RABBITMQ_PORT,
    login=settings.RABBITMQ_USERNAME,
    password=settings.RABBITMQ_PASSWORD,
    apply_types=False,
)
