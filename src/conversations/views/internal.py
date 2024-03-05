from micro.jango.permissions import IsInternal
from micro.jango.serializers import IdSerializer
from micro.jango.views import BaseViewSet, post
from rest_framework import status
from rest_framework.response import Response

from channels.serializers import ChannelSerializer
from conversations.serializers.conversation import (
    ConversationDestroySerializer,
    ConversationJoinSerializer,
    ConversationKickSerializer,
    ConversationMembersSerializer,
)
from conversations.services import ConversationService


class InternalViewSet(BaseViewSet):
    permission_classes = (IsInternal,)
    authentication_classes = ()

    @post(url_path="create")
    def create_(self, request):
        data = request.data.copy()
        serializer = ChannelSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            team_id, creator_id = serializer.extract("team", "creator")
            channel = ConversationService.create_channel(team_id, creator_id, data=serializer.validated_data)
            resp = dict(channel=ChannelSerializer(channel).data)
            return Response(data=resp, status=status.HTTP_200_OK)

    @post(url_path="destroy")
    def destroy_(self, request):
        data = request.data.copy()
        serializer = ConversationDestroySerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            channel_id = serializer.validated_data.pop("channel")
            ConversationService.destroy_channel(channel_id)
            return Response(status=status.HTTP_200_OK)

    @post(url_path="join")
    def join(self, request):
        data = request.data.copy()
        serializer = ConversationJoinSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            channel, _ = ConversationService.join_conversation(serializer.validated_data, publish=False)
            resp = dict(channel=ChannelSerializer(channel).data)
            return Response(resp, status=status.HTTP_200_OK)

    @post(url_path="kick")
    def kick(self, request):
        data = request.data.copy()
        serializer = ConversationKickSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            channel, _ = ConversationService.kick_conversation(serializer.validated_data, publish=False)
            resp = dict(channel=IdSerializer(channel).data)
            return Response(resp, status=status.HTTP_200_OK)

    @post(url_path="members")
    def members(self, request):
        data = request.data.copy()
        serializer = ConversationMembersSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            channel_id = serializer.pop("channel")
            members = ConversationService.list_members(channel_id, **serializer.validated_data)
            return Response(dict(members=list(members)), status=status.HTTP_200_OK)
