from micro.utils import utils

from channels.models import ChannelMember
from tests.internal import InternalTestBase


class TestKickConversation(InternalTestBase):
    def test_kick_from_conversation(self, client):
        user_id = utils.shortid("U")
        channel, _ = self.setup_channel(user_id=user_id)
        member = ChannelMember.objects.filter(channel_id=channel.id, user_id=user_id)
        assert member.exists() is True

        data = dict(channel=channel.id, team=channel.team_id, user=user_id)
        resp = self.client_request(f"{self.URL}/kick", data=data, internal=True, status=200, ok=True)

        assert resp.channel.id == channel.id
        assert member.all().exists() is False
