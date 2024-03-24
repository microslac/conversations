from micro.jango.permissions import IsInternal
from micro.jango.serializers import IdSerializer
from micro.jango.views import BaseViewSet, post
from rest_framework import status
from rest_framework.response import Response

from channels.serializers import ChannelSerializer
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

    @post(url_path="destroy", permission_classes=(IsInternal,))
    def destroy_(self, request):
        data = request.data.copy()
        serializer = IdSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            channel_id = serializer.validated_data.pop("id")
            ConversationService.destroy_channel(channel_id)
            return Response(status=status.HTTP_200_OK)
