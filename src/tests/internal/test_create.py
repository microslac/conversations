import pytest
from micro.utils.utils import shortid

from tests.internal import InternalTestBase


class TestCreateConversation(InternalTestBase):
    @pytest.mark.parametrize("is_private", (False, True))
    def test_create_channel_success(self, is_private):
        team_id, creator_id = shortid("T"), shortid("U")
        data = dict(team=team_id, creator=creator_id, name="channel", is_private=is_private)
        resp = self.client_request(f"{self.URL}/create", data=data, internal=True, status=200, ok=True)

        assert resp.channel.name == "channel"
        assert resp.channel.id.startswith("C")
        assert resp.channel.team == team_id
        assert resp.channel.creator == creator_id
        assert resp.channel.is_channel is True
        assert resp.channel.is_archived is False
        assert resp.channel.is_private == is_private
        assert resp.channel.created is not None
