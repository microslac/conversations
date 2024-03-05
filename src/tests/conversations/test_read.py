import pytest
from tests.conversations import ConversationTestBase


class TestInfoConversation(ConversationTestBase):
    @pytest.mark.parametrize("include_num_members", (True, False))
    def test_info_conversation_success(self, client, include_num_members):
        channel, members = self.setup_channel(num_members=10, team_id="T0123456789")
        data = dict(channel=channel.id, include_num_members=include_num_members)
        resp = self.client_request(f"{self.URL}/info", data=data, status=200, ok=True)

        self.assert_channel(resp.channel, channel)
        if include_num_members:
            assert resp.channel.num_members == len(members)
