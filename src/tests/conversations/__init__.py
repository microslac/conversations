from core.tests import ApiTestBase
from tests.factories import ChannelFactory, ChannelMemberFactory, MessageFactory
from channels.models import Channel


class ConversationTestBase(ApiTestBase):
    URL = "/conversations"

    def assert_channel(self, channel, db_channel: Channel):
        assert channel.id == db_channel.id
        assert channel.team == db_channel.team_id
        assert channel.creator == db_channel.creator_id
        assert channel.is_channel is True
        assert channel.is_archived is False

    def setup_channel(self, num_members: int = 0, user_id: str = None, **data):
        channel = ChannelFactory(**data)
        creator = ChannelMemberFactory(channel_id=channel.id, user_id=channel.creator_id)
        members = [creator.user_id]
        if user_id:  # explicit id
            member = ChannelMemberFactory(channel_id=channel.id, user_id=user_id)
            members.append(member.user_id)
        if num_members:  # random ids
            members.extend([m.user_id for m in ChannelMemberFactory.create_batch(num_members, channel_id=channel.id)])
        return channel, members

    def setup_messages(self, channel: Channel, user_id: str = None, num_messages: int = 10,
                       return_members: bool = False, **data):
        message_data = dict(team_id=channel.team_id, channel_id=channel.id)
        if user_id:
            message_data.update(user_id=user_id)
        messages = MessageFactory.create_batch(num_messages, **message_data)
        members = [ChannelMemberFactory(channel_id=channel.id, user_id=msg.user_id) for msg in messages]
        if return_members:
            return messages, members
        return messages
