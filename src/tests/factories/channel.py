import factory
from factory.django import DjangoModelFactory
from faker import Factory
from core.utils import utils

from channels.models import Channel, ChannelMember

__all__ = ["ChannelFactory", "ChannelMemberFactory"]

fake = Factory.create()


class ChannelFactory(DjangoModelFactory):
    class Meta:
        model = Channel

    name = factory.LazyAttribute(lambda o: fake.company().split().pop(0))
    team_id = factory.LazyAttribute(lambda _: utils.shortid("T"))
    creator_id = factory.LazyAttribute(lambda _: utils.shortid("U"))


class ChannelMemberFactory(DjangoModelFactory):
    class Meta:
        model = ChannelMember

    # channel_id =
    user_id = factory.LazyAttribute(lambda _: utils.shortid("U"))
