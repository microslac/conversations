from contextlib import asynccontextmanager

from django.conf import settings
from faststream.rabbit import RabbitBroker

broker = RabbitBroker(
    host=settings.RABBITMQ_BROKER_HOST,
    port=settings.RABBITMQ_BROKER_PORT,
    login=settings.RABBITMQ_BROKER_USERNAME,
    password=settings.RABBITMQ_BROKER_PASSWORD,
    apply_types=False,
)


@asynccontextmanager
async def lifespan_context(app):
    await broker.start()
    try:
        yield
    finally:
        await broker.close()
