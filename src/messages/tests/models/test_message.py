import uuid

from micro.jango.tests import UnitTestBase

from messages.models import Message
from tests.factories import ChannelFactory, ChannelMemberFactory


class TestMessageModel(UnitTestBase):
    def test_create_message(self):
        user_id = "U0123456789"
        channel = ChannelFactory(creator_id=user_id)
        member = ChannelMemberFactory(channel_id=channel.id, user_id=user_id)
        message = Message.objects.create(
            team_id=channel.team_id,
            user_id=member.user_id,
            channel_id=channel.id,
            client_msg_id=str(uuid.uuid4()),
            text="Hello World",
        )

        assert message.uuid
        assert message.user_id == member.user_id
        assert message.team_id == channel.team_id
        assert message.channel_id == channel.id
        assert message.text == "Hello World"
        assert message.type == "message"
        assert message.subtype == ""
        assert message.ts is not None
