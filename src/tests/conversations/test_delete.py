from tests.conversations import ConversationTestBase
from tests.factories.channel import ChannelFactory


class TestDeleteConversation(ConversationTestBase):
    def test_destroy_channel(self, internal_client):
        channel = ChannelFactory()
        data = dict(id=channel.id)
        self.client_request(f"{self.URL}/destroy", data=data, client=internal_client, status=200, ok=True)
