from django.db.models import Subquery
from micro.jango.exceptions import ApiException
from micro.jango.services import BaseService

from channels.models import Channel, ChannelMember


class ChannelService(BaseService):
    # TODO: cache
    @classmethod
    def get_channel(cls, channel_id: str, default=-1) -> Channel:
        if default != -1:
            return Channel.objects.filter(id=channel_id).first() or default
        return Channel.objects.get(id=channel_id)

    @classmethod
    def create_channel(cls, team_id: str, creator_id: str, **data: dict) -> Channel:
        is_im = data.pop("is_im", False)
        is_mpim = data.pop("is_mpim", False)
        is_channel = data.pop("is_channel", True)
        assert sum([is_im, is_mpim, is_channel]) == 1

        is_general = data.pop("is_general", False)
        is_random = data.pop("is_random", False)
        assert sum([is_random, is_general]) <= 1

        fields = [f.name for f in Channel._meta.fields]  # noqa
        channel_data = {key: value for key, value in data.items() if key in fields}
        channel = Channel.objects.create(
            team_id=team_id,
            creator_id=creator_id,
            is_im=is_im,
            is_mpim=is_mpim,
            is_channel=is_channel,
            is_general=is_general,
            is_random=is_random,
            **channel_data
        )

        return channel

    @classmethod
    def add_member(
        cls, channel: Channel | str, user_id: str = None, user_ids: list[str] = None
    ) -> (ChannelMember | list[ChannelMember]):
        if isinstance(channel, str):
            channel = cls.get_channel(channel)
        if user_id:
            member = ChannelMember.objects.create(channel_id=channel.id, user_id=user_id)
            return member
        if user_ids:
            members = [ChannelMember(channel_id=channel.id, user_id=user_id) for user_id in user_ids]
            return ChannelMember.objecs.bulk_create(members)
        raise Exception()

    @classmethod
    def verify_belong(cls, team_id: str, user_id: str, channel_id, raise_exception: bool = True):
        channel = Channel.objects.filter(id=channel_id, team_id=team_id)
        member = ChannelMember.objects.filter(channel_id=Subquery(channel.values("id")), user_id=user_id)
        is_belong = member.exists()
        if not is_belong and raise_exception:
            raise ApiException(error="not_in_channel")
        return is_belong
