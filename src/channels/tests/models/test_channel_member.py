import pytest
from django.db import IntegrityError
from micro.jango.tests import UnitTestBase
from micro.utils import utils

from channels.models import ChannelMember
from tests.factories import ChannelFactory


class TestChannelMemberModel(UnitTestBase):
    def test_channel_members(self):
        channel = ChannelFactory()
        user_ids = [channel.creator_id] + [utils.shortid("U") for _ in range(9)]
        members = [ChannelMember.objects.create(channel_id=channel.id, user_id=user_id) for user_id in user_ids]

        assert {channel.id} == {member.channel_id for member in members}
        assert sorted(channel.members) == sorted(member.user_id for member in members)

    def test_channel_duplicated_members(self):
        channel = ChannelFactory()
        user_id = utils.shortid("U")
        ChannelMember.objects.create(channel_id=channel.id, user_id=user_id)

        with pytest.raises(IntegrityError):
            ChannelMember.objects.create(channel_id=channel.id, user_id=user_id)
