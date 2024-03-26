from rest_framework import serializers
from micro.jango.exceptions import ApiException
from micro.jango.serializers import BaseSerializer, TimestampField


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


class ConversationJoinSerializer(BaseSerializer):
    team = serializers.CharField(required=True, allow_blank=False)
    user = serializers.CharField(required=True, allow_blank=False)
    channel = serializers.CharField(required=False, allow_blank=True, default="")
    is_general = serializers.BooleanField(required=False, default=False)
    is_random = serializers.BooleanField(required=False, default=False)

    def validate(self, data: dict):
        bools = [bool(v) for k, v in data.items() if k in {"channel", "is_general", "is_random"}]

        if sum(bools) != 1:
            raise ApiException(error="too_many_values")
        return data


class ConversationMembersSerializer(BaseSerializer):
    channel = serializers.CharField(required=True, allow_blank=False)
    all_members = serializers.BooleanField(required=False, default=False)
