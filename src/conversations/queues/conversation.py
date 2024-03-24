from micro.jango.queues import BaseQueue
from pika.channel import Channel
from pika.exchange_type import ExchangeType


class ConversationQueue(BaseQueue):
    _exchange = "conversations"

    @classmethod
    def get_exchange(cls) -> str:
        return cls._exchange

    @classmethod
    def get_channel(cls) -> Channel:
        return cls._channel

    @classmethod
    def declare_exchange(cls, exchange_type: ExchangeType = ExchangeType.topic, **kwargs):
        exchange = cls.get_exchange()
        channel = cls.get_channel()
        channel.exchange_declare(exchange, exchange_type=exchange_type, **kwargs)
