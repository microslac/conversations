import pytest
from micro.utils import utils

from channels.models import ChannelMember
from tests.factories.channel import ChannelFactory
from tests.internal import InternalTestBase


class TestJoinConversation(InternalTestBase):
    def test_join_channel_by_id(self, client):
        channel = ChannelFactory()
        team_id = channel.team_id
        user_id = utils.shortid("U")
        data = dict(channel=channel.id, team=team_id, user=user_id)
        resp = self.client_request(f"{self.URL}/join", data=data, internal=True, status=200, ok=True)

        assert resp.channel.id == channel.id
        assert ChannelMember.objects.filter(channel_id=channel.id, user_id=user_id).exists() is True

    @pytest.mark.parametrize("values", [(True, False), (False, True)])
    def test_join_channel_by_attr(self, values):
        is_general, is_random = values
        team_id = utils.shortid("T")
        user_id = utils.shortid("U")
        channel = ChannelFactory(team_id=team_id, is_general=is_general, is_random=is_random)
        data = dict(team=team_id, user=user_id, is_general=is_general, is_random=is_random)
        resp = self.client_request(f"{self.URL}/join", data=data, internal=True, status=200, ok=True)

        assert resp.channel.id == channel.id
        assert ChannelMember.objects.filter(channel_id=channel.id, user_id=user_id).exists() is True
