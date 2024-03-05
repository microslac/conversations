from uuid import uuid4
from tests.conversations import ConversationTestBase


class TestPostConversation(ConversationTestBase):
    def test_post_conversation_success(self, client):
        team_id, user_id = client.token.team, client.token.user
        channel, members = self.setup_channel(team_id=team_id, creator_id=user_id)
        data = dict(channel=channel.id, text=self.fake.text(), client_msg_id=str(uuid4()))
        resp = self.client_request(f"{self.URL}/post", data=data, status=200, ok=True)

        assert resp.ts is not None
        assert resp.channel == channel.id
        assert resp.message.user == user_id
        assert resp.message.team == team_id
        assert resp.message.ts is not None
        assert resp.message.text == data["text"]
        assert resp.message.type == "message"
        assert not getattr(resp.message, "subtype", None)
        assert resp.message.client_msg_id == data["client_msg_id"]
