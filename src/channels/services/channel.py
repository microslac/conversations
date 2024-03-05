from django.db.models import Q, QuerySet, Subquery
from micro.jango.exceptions import ApiException
from micro.jango.services import BaseService

from channels.models import Channel, ChannelMember


class ChannelService(BaseService):
    # TODO: cache
    @classmethod
    def get_channel(cls, channel_id: str, nullable: bool = False, **kwargs) -> Channel:
        query = Q(id=channel_id, **kwargs)
        if nullable:
            return Channel.objects.filter(query).first()
        return Channel.objects.get(query)

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
            return ChannelMember.objects.bulk_create(members)
        raise Exception()

    @classmethod
    def remove_member(cls, channel: Channel | str, user_id: str = None, user_ids: list[str] = None):
        if isinstance(channel, str):
            channel = cls.get_channel(channel)

        user_ids = user_ids or [user_id]
        members: QuerySet[ChannelMember] = ChannelMember.objects.filter(channel_id=channel.id, user_id__in=user_ids)
        return members.delete()

    @classmethod
    def verify_belong(cls, team_id: str, user_id: str, channel_id, raise_exception: bool = True):
        channel = Channel.objects.filter(id=channel_id, team_id=team_id)
        member = ChannelMember.objects.filter(channel_id=Subquery(channel.values("id")), user_id=user_id)
        is_belong = member.exists()
        if not is_belong and raise_exception:
            raise ApiException(error="not_in_channel")
        return is_belong

    @classmethod
    def get_base_channels(cls, team_id: str) -> QuerySet[Channel]:
        query = Q(is_general=True) | Q(is_random=True)
        query = Q(team_id=team_id) & query
        return Channel.objects.filter(query)
