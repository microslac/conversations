from micro.jango.tests import UnitTestBase

from channels.models import Channel


class TestChannelModel(UnitTestBase):
    def test_create_channel(self):
        team_id, creator_id, name = "T0123456789", "U0123456789", "channel"
        channel = Channel.channels.create(team_id=team_id, creator_id=creator_id, name=name)

        assert channel.uuid
        assert channel.id.startswith("C")
        assert channel.name == name
        assert channel.team_id == team_id
        assert channel.creator_id == creator_id
        assert channel.created is not None

        assert channel.is_channel is True
        assert channel.is_mpim is False
        assert channel.is_im is False
