import pytest
from tests.conversations import ConversationTestBase


class TestViewConversation(ConversationTestBase):
    @pytest.mark.parametrize("specify_channel", (True, False))
    def test_view_conversation_success(self, client, specify_channel):
        team_id, user_id = client.token.team, client.token.user  # TODO: credentials: jwt()
        general_channel, general_members = self.setup_channel(
            team_id=team_id,
            creator_id=user_id,
            num_members=30,
            is_general=True)
        random_channel, random_members = self.setup_channel(
            team_id=team_id,
            creator_id=user_id,
            num_members=30,
            is_random=True
        )

        general_messages = self.setup_messages(channel=general_channel, num_messages=50)
        random_messages = self.setup_messages(channel=random_channel, num_messages=50)

        limit = 28
        data = dict(channel=random_channel.id if specify_channel else None, limit=limit)
        resp = self.client_request(f"{self.URL}/view", data=data, status=200, ok=True)

        channel = random_channel if specify_channel else general_channel
        messages: list = random_messages if specify_channel else general_messages
        ordered_messages = sorted(messages, key=lambda m: m.ts, reverse=True)

        assert resp.channel.id == channel.id
        assert resp.channel.name == channel.name
        assert resp.channel.team == channel.team_id
        assert set(resp.user_ids) == set([m.user_id for m in ordered_messages[:limit]])
