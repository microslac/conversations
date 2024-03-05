from datetime import datetime

from django.db.models import Q
from faststream.rabbit import ExchangeType, RabbitExchange, RabbitQueue

from channels.models import Channel, ChannelMember
from conversations import utils
from conversations.broker import broker
from messages.constants import MessageSubType, MessageType
from messages.models import Message
from messages.serializers import MessageSerializer

exchange = RabbitExchange("communication", type=ExchangeType.TOPIC)
team_user_queue = RabbitQueue("conversations.team.user.event", routing_key="team.user.{event}")


@broker.subscriber(team_user_queue, exchange=exchange)
async def team_user_joined_handler(data: dict):
    team_id = data.pop("team")
    user_id = data.pop("user")

    query = Q(is_general=True) | Q(is_random=True)
    query = Q(team_id=team_id) & query
    base_channels = Channel.objects.filter(query)

    async for channel in base_channels:
        members = ChannelMember.objects.filter(channel=channel.id)
        member_ids = [member.user_id async for member in members]
        member = await ChannelMember.objects.filter(user_id=user_id).afirst()
        payload = dict(
            user=member.user_id,
            team=channel.team_id,
            channel=channel.id,
            channel_type=channel.id[0],
            ts=utils.to_timestamp(member.created),
            event_ts=utils.to_timestamp(datetime.utcnow()),
            members=list(member_ids),
        )
        await broker.publish(payload, exchange=exchange, queue="channel.member.joined")

        joined_messages = Message.objects.filter(
            user_id=user_id,
            channel_id=channel.id,
            type=MessageType.MESSAGE,
            subtype=MessageSubType.CHANNEL_JOINED,
        )

        async for message in joined_messages:
            payload = dict(
                user=message.user_id,
                members=list(member_ids),
                channel=message.channel_id,
                message=MessageSerializer(message).data,
            )
            await broker.publish(payload, exchange=exchange, queue="message")
