from __future__ import annotations

import json

import pika
from django.conf import settings
from micro.jango.services import BaseService
from pika.channel import Channel
from pika.connection import Connection


class ConnectionDescriptor:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5672,
        username: str = "user",
        password: str = "password",
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, cls: type[RealtimeService]):
        if instance is None:
            assert all([self.host, self.port, self.username, self.password])

            credentials = pika.PlainCredentials(username=self.username, password=self.password)
            parameters = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
            connection = pika.BlockingConnection(parameters=parameters)
            setattr(cls, self.name, connection)
        raise RuntimeError("Cannot access class attributes from concrete instance.")


class ChannelDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, cls: type[RealtimeService]):
        if instance is None:
            channel = cls._connection.channel()
            setattr(cls, self.name, channel)
        raise RuntimeError("Cannot access class attributes from concrete instance.")


class RealtimeService(BaseService):
    _connection: Connection = ConnectionDescriptor(
        host=settings.MICROSERVICE.REALTIME_QUEUE_HOST,
        port=settings.MICROSERVICE.REALTIME_QUEUE_PORT,
        username=settings.MICROSERVICE.REALTIME_QUEUE_USERNAME,
        password=settings.MICROSERVICE.REALTIME_QUEUE_PASSWORD,
    )
    _channel: Channel = ChannelDescriptor()
    _exchange: str = "conversations"

    @classmethod
    def publish(
        cls,
        queue: str = "message.created",
        data: dict = None,
        exchange: str = "",
        properties: pika.BasicProperties = None,
        **kwargs,
    ):
        data = data or {}
        body = json.dumps(data).encode("utf-8")
        properties = properties or pika.BasicProperties(content_type="application/json", content_encoding="utf-8")
        cls._channel.basic_publish(exchange=exchange, routing_key=queue, body=body, properties=properties)
