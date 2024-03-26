from datetime import datetime
from typing import Optional

from django.db import transaction
from django.db.models import Q
from micro.jango.services import BaseService
from micro.events.registry import CommunicationEvents
from micro.utils import utils

from channels.models import Channel, ChannelMember
from channels.services import ChannelService
from conversations.utils import decode_cursor, encode_cursor
from messages.models import Message

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
        channel.destroy()
        return channel_id

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
    def post_message(cls, data: dict, publish: bool = False) -> Message:
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
        member_ids = cls.get_channel(message.channel_id).members
        payload = dict(
            user=message.user_id,
            users=list(member_ids),
            channel=message.channel_id,
            message=MessageSerializer(message).data,
        )
        CommunicationEvents.publish(payload, routing_key="message")

    @classmethod
    def join_conversation(cls, data: dict, publish: bool = False) -> tuple[Channel, ChannelMember]:
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
        if publish:
            cls.publish_join_conversation(channel.id, user_id)

        return channel, member

    @classmethod
    def publish_join_conversation(cls, channel_id: str, user_id: str):
        payload = dict(channel=channel_id, user=user_id)
        CommunicationEvents.publish(payload, routing_key="channel.member.joined")

    @classmethod
    def list_members(cls, channel_id: str, **kwargs):
        limit = kwargs.pop("limit", 100)
        cursor = kwargs.pop("cursor", "")
        all_members = kwargs.pop("all_members", False)
        channel = ChannelService.get_channel(channel_id)

        if all_members:
            return channel.members
        return channel.members, f"{limit}:{cursor}"
