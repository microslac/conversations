from rest_framework import serializers

from messages.models import Message

from core.serializers import BaseModelSerializer, TimestampField


class MessageSerializer(BaseModelSerializer):
    team_id = serializers.CharField(required=True, allow_blank=False, write_only=True)
    user_id = serializers.CharField(required=True, allow_blank=False, write_only=True)
    channel_id = serializers.CharField(required=True, allow_blank=False, write_only=True)
    text = serializers.CharField(required=True, allow_blank=False)
    updated = TimestampField(required=False, read_only=True)
    ts = TimestampField(required=False, read_only=True)

    class Meta:
        model = Message
        fields = ("team_id", "user_id", "channel_id", "text",
                  "client_msg_id", "type", "subtype", "metadata", "ts", "updated")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        nullable_fields = {"subtype", "metadata", "client_msg_id"}
        data = {k: v for k, v in data.items() if k not in nullable_fields or bool(v)}
        data.update(team=instance.team_id, user=instance.user_id, channel=instance.channel_id)
        if fields := self.context.get("fields", {}):
            data = {k: v for k, v in data.items() if k in fields}
        if exclude_fields := self.context.get("exclude_fields", {}):
            data = {k: v for k, v in data.items() if k not in exclude_fields}
        return data
