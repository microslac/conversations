from random import randint

from tests.internal import InternalTestBase


class TestConversationMembers(InternalTestBase):
    def test_conversation_members(self, client):
        num_members = randint(20, 30)
        channel, members = self.setup_channel(num_members=num_members)
        data = dict(channel=channel.id, all_members=True)
        resp = self.client_request(f"{self.URL}/members", data=data, internal=True, status=200, ok=True)

        assert sorted(resp.members) == sorted(members)
