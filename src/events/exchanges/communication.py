from django.db.models import Q
from faststream.rabbit import RabbitExchange, RabbitQueue, ExchangeType
from channels.models import Channel
from events.broker import broker
from messages.models import Message
from messages.constants import MessageType, MessageSubType
from channels.models import ChannelMember
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

        payload = dict(channel=channel.id, user=user_id, members=list(member_ids))
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
