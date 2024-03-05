import math

import pytest
import base64
from tests.conversations import ConversationTestBase


class TestHistoryConversation(ConversationTestBase):
    @pytest.mark.parametrize("num_messages", (20, 50))
    def test_history_conversation_success(self, client, num_messages):
        team_id, user_id = client.token.team, client.token.user  # TODO: credentials: jwt()
        channel, members = self.setup_channel(
            team_id=team_id,
            creator_id=user_id,
            num_members=30,
            is_general=True)
        messages = self.setup_messages(channel, num_messages=num_messages)

        limit = 28
        data = dict(channel=channel.id, limit=limit)
        resp = self.client_request(f"{self.URL}/history", data=data, status=200, ok=True)

        assert resp.has_more == (num_messages > limit)
        assert len(resp.messages) == min(limit, len(messages))
        if next_cursor := resp.response_metadata.next_cursor:
            next_timestamp = f"next_ts:{math.trunc(messages[limit + 1].timestamp)}"
            assert base64.b64decode(next_cursor).decode("utf-8").startswith(next_timestamp)
