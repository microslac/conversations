import pytest
from tests.conversations import ConversationTestBase


class TestCreateConversation(ConversationTestBase):
    @pytest.mark.parametrize("is_private", (False, True))
    def test_create_channel_success(self, client, is_private):
        data = dict(name="channel", is_private=is_private)
        resp = self.client_request(f"{self.URL}/create", data=data, status=200, ok=True)

        assert resp.channel.name == "channel"
        assert resp.channel.id.startswith("C")
        assert resp.channel.team == "T0123456789"  # jwt
        assert resp.channel.creator == "U0123456789"  # jwt
        assert resp.channel.is_channel is True
        assert resp.channel.is_archived is False
        assert resp.channel.is_private == is_private
        assert resp.channel.created is not None

