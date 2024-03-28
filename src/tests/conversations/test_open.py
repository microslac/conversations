import pytest
from channels.models import Channel
from micro.utils import utils
from tests.conversations import ConversationTestBase


class TestOpenConversation(ConversationTestBase):
    @pytest.mark.parametrize("return_im,num_users", [(False, 2), (True, 2)])
    def test_open_im_conversation(self, client, return_im, num_users):
        team_id, creator_id, other_id = client.token.team, client.token.user, utils.shortid("U")
        data = dict(team=team_id, user=creator_id, users=[other_id], return_im=return_im)
        resp = self.client_request(f"{self.URL}/open", data=data, status=200, ok=True)

        assert resp.already_open is False
        assert resp.channel.id.startswith("D")  # im_channel
        if return_im:
            assert resp.channel.is_im is True
            assert resp.channel.is_mpim is False
            assert resp.channel.is_channel is False
            assert resp.channel.creator == creator_id
            assert resp.channel.user == other_id
            assert resp.channel.team == team_id

        channel: Channel = Channel.objects.get(pk=resp.channel.id)
        assert set(channel.member_ids) == {creator_id, other_id}
