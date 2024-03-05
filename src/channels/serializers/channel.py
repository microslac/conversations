from rest_framework import serializers
from core.serializers import BaseModelSerializer, TimestampField
from channels.models import Channel


class ChannelSerializer(BaseModelSerializer):
    team_id = serializers.CharField(required=True, write_only=True)
    creator_id = serializers.CharField(required=True, write_only=True)
    updater_id = serializers.CharField(required=False, write_only=True)
    created = TimestampField(required=False, read_only=True)
    updated = TimestampField(required=False, read_only=True)

    class Meta:
        model = Channel
        fields = (
            "id",
            "name",
            "team_id",
            "is_im",
            "is_mpim",
            "is_channel",
            "is_general",
            "is_random",
            "is_archived",
            "is_frozen",
            "is_private",
            "is_shared",
            "is_read_only",
            "created",
            "updated",
            "creator_id",
            "updater_id",
        )

    def to_representation(self, instance: Channel):
        data = super().to_representation(instance)
        data.update(team=instance.team_id)
        data.update(creator=instance.creator_id)
        data.update(updater=instance.updater_id)
        if instance.is_im and (exclude_id := self.context.get("exclude_id")):
            member_ids = list(instance.members)
            member_ids.remove(exclude_id)
            other_id = next(iter(member_ids))
            data.update(user=other_id)
        if self.context.get("include_num_members", False):
            data.update(num_members=instance.members.count())
        if self.context.get("include_members", False):
            data.update(members=list(instance.members))
        return data
