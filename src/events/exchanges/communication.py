from django.db.models import Q
from faststream.rabbit import RabbitExchange, RabbitQueue, ExchangeType
from conversations.services import ConversationService
from channels.models import Channel
from events.broker import broker

exchange = RabbitExchange("communication", type=ExchangeType.TOPIC)
team_user_queue = RabbitQueue("", routing_key="team.user.{event}")


@broker.subscriber(team_user_queue, exchange=exchange)
async def handle_user_join_team(data: dict):
    team_id = data.pop("team")
    user_id = data.pop("user")

    query = Q(is_general=True) | Q(is_random=True)
    query = Q(team_id=team_id) & query
    qs = Channel.objects.filter(query)
    base_channels = [channel async for channel in qs]

    for channel in base_channels:
        ConversationService.publish_join_conversation(channel.id, user_id=user_id)
