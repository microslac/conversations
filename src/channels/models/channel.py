from django.db import models
from django.db.models import QuerySet
from django.db.models.functions import Lower
from django.db.models.manager import Manager
from django.utils.functional import cached_property
from micro.jango.models import DeletedModel, HistoryModel, UUIDModel
from micro.jango.models.fields import ShortIdField

from channels.managers import ChannelManager
from channels.querysets import ChChannelQuerySet, ImChannelQuerySet, MpimChannelQuerySet


class Channel(UUIDModel, DeletedModel, HistoryModel):
    id = ShortIdField(prefix="C", primary_key=True)
    name = models.CharField(max_length=255, db_index=True)
    team_id = models.CharField(blank=False, max_length=20, db_index=True)

    is_im = models.BooleanField(default=False)
    is_mpim = models.BooleanField(default=False)
    is_channel = models.BooleanField(default=True)

    is_general = models.BooleanField(default=False)
    is_random = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_frozen = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)
    is_read_only = models.BooleanField(default=False)

    objects = ChannelManager()
    channels: Manager = ChChannelQuerySet.as_manager()
    ims: Manager = ImChannelQuerySet.as_manager()
    mpims: Manager = MpimChannelQuerySet.as_manager()

    class Meta:
        db_table = "channels"
        constraints = [
            models.UniqueConstraint(Lower("name"), "team_id", name="unique_channel_name"),
        ]
        ordering = ["-created"]

    @cached_property
    def members(self) -> QuerySet:
        from channels.models import ChannelMember

        return ChannelMember.objects.filter(channel=self.id).values_list("user_id", flat=True)
