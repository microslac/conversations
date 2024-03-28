from contextlib import suppress
from datetime import datetime
from typing import Optional

from django.db import transaction
from django.db.models import Q
from micro.jango.services import BaseService
from micro.utils import utils
from micro.jango.exceptions import ApiException

from channels.models import Channel, ChannelMember
from channels.services import ChannelService
from conversations.utils import decode_cursor, encode_cursor, enquote
from conversations.services.publishers import communication
from messages.models import Message
from messages.constants import MessageType, MessageSubType

from messages.serializers import MessageSerializer


class ConversationService(BaseService):
    @classmethod
    def create_channel(cls, team_id: str, creator_id: str, data: dict) -> Channel:
        with transaction.atomic():
            channel = ChannelService.create_channel(team_id, creator_id, **data)
            ChannelService.add_member(channel, user_id=channel.creator_id)
        return channel

    @classmethod
    def destroy_channel(cls, channel_id: str) -> str:
        channel = Channel.objects.get(id=channel_id)
        messages = Message.objects.filter(channel_id=channel.id)
        members = ChannelMember.objects.filter(channel_id=channel.id)
        channel.destroy()
        messages.destroy()
        members.delete()

        return channel.id

    @classmethod
    def get_channel(cls, channel_id: str, team_id: str = None, **kwargs) -> Optional[Channel]:
        channel_qs = Channel.objects.filter(id=channel_id)
        if team_id:
            channel_qs = channel_qs.filter(team_id=team_id)
        return channel_qs.first()

    @classmethod
    def get_history(cls, team_id, channel_id: str, **kwargs) -> tuple:
        channel = Channel.objects.get(id=channel_id, team_id=team_id)
        inclusive = kwargs.get("inclusive", False)
        limit = utils.safe_int(kwargs.get("limit"), default=100, max_=500)

        messages_q = Q(team_id=team_id, channel_id=channel.id)

        if latest := kwargs.get("latest"):
            latest_q = Q(ts__lte=latest) if inclusive else Q(ts__lt=latest)
            messages_q &= latest_q
        if oldest := kwargs.get("oldest"):
            oldest_q = Q(ts__gte=oldest) if inclusive else Q(ts__gt=oldest)
            messages_q &= oldest_q
        if cursor := kwargs.get("cursor"):
            from_ts = decode_cursor(cursor, scheme="next_ts", parser=(float, datetime.utcfromtimestamp))
            messages_q &= Q(ts__lte=from_ts)

        messages = Message.objects.filter(messages_q)
        messages: list[Message] = list(messages[: limit + 1])

        if len(messages) > limit:
            next_message = messages.pop()
            next_cursor = encode_cursor(f"next_ts:{next_message.timestamp}")
            next_ts = next_message.timestamp
        else:
            next_cursor = ""
            next_ts = None

        return messages, next_cursor, next_ts

    @classmethod
    def view_conversation(cls, team_id: str, channel_id: str, **kwargs) -> tuple:
        limit = kwargs.pop("limit", None)

        # TODO: filter channels that the user belong to
        query = Q(team_id=team_id, id=channel_id) | Q(team_id=team_id, is_general=True)
        channel = Channel.objects.filter(query).first()
        channels = [channel]  # TODO

        messages, next_cursor, next_ts = cls.get_history(team_id, channel.id, limit=limit)
        user_ids = [msg.user_id for msg in messages]

        return channel, channels, user_ids, messages, next_cursor, next_ts

    @classmethod
    def post_message(cls, data: dict, publish: bool = True) -> Message:
        tid, uid, cid = utils.extract(data, "team_id", "user_id", "channel_id", how="get")
        ChannelService.verify_belong(tid, uid, cid)

        data = data or {}
        fields = {f.name for f in Message._meta.fields}  # noqa
        data = {key: value for key, value in data.items() if key in fields}
        message = Message.objects.create(**data)
        if publish:
            cls.publish_message(message)

        return message

    @classmethod
    def publish_message(cls, message: Message):
        member_ids = cls.get_channel(message.channel_id).member_ids
        payload = dict(
            user=message.user_id,
            members=list(member_ids),
            channel=message.channel_id,
            message=MessageSerializer(message).data,
        )
        communication.publish(payload, routing_key="message")

    @classmethod
    def join_conversation(cls, data: dict, publish: bool = True) -> tuple[Channel, ChannelMember]:
        team_id = data.pop("team")
        user_id = data.pop("user")
        channel_id = data.pop("channel", "")
        is_random = data.pop("is_random", False)
        is_general = data.pop("is_general", False)

        if is_general:
            query = Q(is_general=is_general)
        elif is_random:
            query = Q(is_random=is_random)
        else:
            query = Q(id=channel_id)

        query = query & Q(team_id=team_id)
        channel = Channel.objects.filter(query).first()
        member = ChannelService.add_member(channel, user_id)
        joined_message = cls.create_joined_message(channel.team_id, channel.id, user_id)
        if publish:
            cls.publish_joined_conversation(channel.id, user_id)
            cls.publish_message(joined_message)

        return channel, member

    @classmethod
    def create_joined_message(cls, team_id: str, channel_id: str, user_id: str) -> Message:
        text = f"{enquote(user_id)} has joined the channel"
        message = Message.objects.create(
            text=text,
            team_id=team_id,
            user_id=user_id,
            channel_id=channel_id,
            type=MessageType.MESSAGE,
            subtype=MessageSubType.CHANNEL_JOINED,
        )
        return message

    @classmethod
    def publish_joined_conversation(cls, channel_id: str, user_id: str):
        payload = dict(channel=channel_id, user=user_id)
        communication.publish(payload, routing_key="channel.member.joined")

    @classmethod
    def kick_conversation(cls, data: dict, publish=True):
        team_id = data.pop("team")
        user_id = data.pop("user")
        channel_id = data.pop("channel", "")
        channel = ChannelService.get_channel(channel_id, team_id=team_id)
        result = ChannelService.remove_member(channel, user_id=user_id)
        return channel, result

    @classmethod
    def list_members(cls, channel_id: str, **kwargs):
        limit = kwargs.pop("limit", 100)
        cursor = kwargs.pop("cursor", "")
        all_members = kwargs.pop("all_members", False)
        channel = ChannelService.get_channel(channel_id)

        if all_members:
            return channel.member_ids
        return channel.member_ids, f"{limit}:{cursor}"

    @classmethod
    def open_channel(
            cls, team_id: str, creator_id: str, channel_id: str = None, user_ids: list = None, data: dict = None
    ) -> tuple[Channel, bool]:
        if channel_id:
            channel = cls.get_channel(channel_id, team_id=team_id)
            if not channel:
                raise ApiException(error="channel_not_found")
            return channel, False

        if not user_ids:
            raise ApiException("user_not_supplied")
        elif len(user_ids) > 1:
            return cls.open_mpim_channel(team_id, creator_id, user_ids=user_ids, data=data)
        else:
            return cls.open_im_channel(team_id, creator_id, user_ids.pop(), data=data)

    @classmethod
    def open_mpim_channel(
            cls, team_id: str, creator_id: str, *, user_ids: list[str], data: dict = None
    ) -> tuple[Channel, bool]:
        user_ids = set(sorted(user_ids))

        if len(user_ids) > 8:
            raise ApiException("too_many_users")
        elif len(user_ids) <= 2:
            raise ApiException(error="not_enough_users")
        # elif TODO: lookup
        # raise ApiException(error="user_not_found", users=list(null_ids))

        with transaction.atomic():
            joined_names = "--".join([user_id for user_id in user_ids])
            mpim_channel, created = Channel.mpims.get_or_create(
                team_id=team_id,
                name=f"mpim-{joined_names}",
                creator_id=creator_id,
            )
            if created:
                mpim_channel.add_members(user_ids=[*user_ids, creator_id])
            return mpim_channel, created

    @classmethod
    def open_im_channel(cls, team_id: str, creator_id: str, other_id: str, data: dict = None) -> tuple[Channel, bool]:
        with transaction.atomic():
            user_ids = list(sorted([creator_id, other_id]))
            joined_names = "--".join([user_id for user_id in user_ids])
            im_channel, created = Channel.ims.get_or_create(team_id=team_id, name=f"im-{joined_names}")
            if created:
                im_channel.creator_id = creator_id
                im_channel.add_members(user_ids=user_ids)
                im_channel.save(update_fields=["creator_id"])
            return im_channel, created
