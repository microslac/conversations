from django.db import models

from core.models.history import HistoryModel
from channels.models import Channel


class ChannelMember(HistoryModel):
    # TODO:
    #  - channel delete event
    #  - user deleted event
    user_id = models.CharField(max_length=20, null=False, blank=False)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    class Meta:
        db_table = "channel_members"
        unique_together = ("channel_id", "user_id")
