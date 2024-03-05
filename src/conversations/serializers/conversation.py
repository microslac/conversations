from rest_framework import serializers
from core.serializers import BaseSerializer, TimestampField


class ConversationInfoSerializer(BaseSerializer):
    channel = serializers.CharField(required=True, allow_blank=False)
    include_num_members = serializers.BooleanField(required=False, default=False)


class ConversationHistorySerializer(BaseSerializer):
    channel = serializers.CharField(required=True, allow_blank=False)
    cursor = serializers.CharField(required=False, allow_blank=True, default="")
    limit = serializers.IntegerField(required=False, default=100, max_value=1000)
    inclusive = serializers.BooleanField(required=False, default=False)
    latest = TimestampField(required=False)
    oldest = TimestampField(required=False)


class ConversationViewSerializer(BaseSerializer):
    channel = serializers.CharField(required=False, allow_null=True, allow_blank=True, default="")
    limit = serializers.IntegerField(required=False, default=28)  # TODO: const
