from micro.jango.views import BaseViewSet, post
from rest_framework import status
from rest_framework.response import Response

from channels.serializers import ChannelSerializer
from conversations.serializers import (
    ConversationHistorySerializer,
    ConversationInfoSerializer,
    ConversationViewSerializer,
)
from conversations.services import ConversationService
from messages.serializers import MessageSerializer


class ConversationViewSet(BaseViewSet):
    @post(url_path="create")
    def create_(self, request):
        data = request.data.copy()
        team_id = request.token.team
        creator_id = request.token.user
        data.update(team_id=team_id, creator_id=creator_id)
        serializer = ChannelSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            channel = ConversationService.create_channel(team_id, creator_id, data=serializer.validated_data)
            resp = dict(channel=ChannelSerializer(channel).data)
            return Response(data=resp, status=status.HTTP_200_OK)

    @post(url_path="info")
    def info(self, request):
        data = request.data.copy()
        team_id, user_id = request.token.team, request.token.user
        serializer = ConversationInfoSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            channel_id, include_num_members = serializer.extract()
            channel = ConversationService.get_channel(channel_id, team_id)
            context = dict(exclude_id=user_id) if channel.is_im else dict(include_num_members=include_num_members)
            resp = dict(channel=ChannelSerializer(channel, context=context).data)
            return Response(data=resp, status=status.HTTP_200_OK)

    @post(url_path="post")
    def post_(self, request):
        data = request.data.copy()
        tid, uid, cid = request.token.team, request.token.user, data.pop("channel", None)
        data.update(team_id=tid, user_id=uid, channel_id=cid)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            message = ConversationService.post_message(data=serializer.validated_data, publish=True)
            resp = dict(ts=message.timestamp, channel=message.channel_id, message=MessageSerializer(message).data)
            return Response(data=resp, status=status.HTTP_200_OK)

    @post(url_path="history")
    def history(self, request):
        data = request.data.copy()
        team_id = request.token.team
        serializer = ConversationHistorySerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            channel_id = serializer.pop("channel")
            messages, next_cursor, next_ts = ConversationService.get_history(
                team_id, channel_id, **serializer.validated_data
            )
            resp = dict(
                messages=MessageSerializer(messages, many=True).data,
                response_metadata=dict(next_cursor=next_cursor),
                has_more=bool(next_cursor),
            )
            return Response(resp, status=status.HTTP_200_OK)

    @post(url_path="view")
    def view(self, request):
        data = request.data.copy()
        team_id = request.token.team
        serializer = ConversationViewSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            channel_id, limit = serializer.extract("channel", "limit")
            channel, channels, user_ids, messages, next_cursor, next_ts = ConversationService.view_conversation(
                team_id, channel_id, limit=limit
            )
            resp = dict(
                channel=ChannelSerializer(channel).data,
                channels=ChannelSerializer(channels, many=True).data,
                user_ids=user_ids,
                history=dict(
                    messages=MessageSerializer(messages, many=True).data,
                    has_more=bool(next_cursor),
                    next_ts=next_ts,
                ),
                response_metadata=dict(next_cursor=next_cursor),
            )
            return Response(resp, status.HTTP_200_OK)
