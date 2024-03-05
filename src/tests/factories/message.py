import factory
from factory.django import DjangoModelFactory
from faker import Factory
from core.utils import utils

from messages.models import Message

__all__ = ["MessageFactory", ]

fake = Factory.create()


class MessageFactory(DjangoModelFactory):
    class Meta:
        model = Message

    team_id = factory.LazyAttribute(lambda _: utils.shortid("T"))
    user_id = factory.LazyAttribute(lambda _: utils.shortid("U"))
    channel_id = factory.LazyAttribute(lambda _: utils.shortid("C"))

    text = factory.LazyAttribute(lambda _: fake.text())
