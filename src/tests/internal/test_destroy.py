from tests.factories.channel import ChannelFactory
from tests.internal import InternalTestBase


class TestDestroyConversation(InternalTestBase):
    def test_destroy_channel(self):
        channel = ChannelFactory()
        data = dict(channel=channel.id)
        self.client_request(f"{self.URL}/destroy", data=data, internal=True, status=200, ok=True)

        # assert Channel.objects.filter(id=channel.id).exists() is False
