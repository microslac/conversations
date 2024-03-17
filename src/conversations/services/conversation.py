from datetime import datetime
from typing import Optional
from core.services import BaseService
from channels.models import Channel
from channels.services import ChannelService
from messages.models import Message
from django.db import transaction
from core.utils import utils
from conversations.utils import encode_cursor, decode_cursor
from django.db.models import Q


class ConversationService(BaseService):
    @classmethod
    def create_channel(cls, data: dict) -> Channel:
        with transaction.atomic():
            channel = ChannelService.create_channel(**data)
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
    def get_history(cls, team_id, channel_id: str, **kwargs):
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
    def view_channel(cls, team_id: str, channel_id: str, **kwargs):
        limit = kwargs.pop("limit", None)

        # TODO: filter channels that the user belong to
        query = Q(team_id=team_id, id=channel_id) | Q(team_id=team_id, is_general=True)
        channel = Channel.objects.filter(query).first()
        channels = [channel]  # TODO

        messages, next_cursor, next_ts = cls.get_history(team_id, channel.id, limit=limit)
        user_ids = [msg.user_id for msg in messages]

        return channel, channels, user_ids, messages, next_cursor, next_ts

    @classmethod
    def post_message(cls, data: dict):
        tid, uid, cid = utils.extract(data, "team_id", "user_id", "channel_id", how="get")
        ChannelService.verify_belong(tid, uid, cid)

        data = data or {}
        fields = {f.name for f in Message._meta.fields}  # noqa
        data = {key: value for key, value in data.items() if key in fields}
        message = Message.objects.create(**data)
        # cls.publish_message(message)  # TODO: message_created queue
        return message
