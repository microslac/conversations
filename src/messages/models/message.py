from django.db import models
from micro.jango.models import DeletedModel, HistoryModel, UUIDModel
from micro.utils import utils

from messages.constants import MessageSubType, MessageType
from messages.managers import MessageManager


class Message(UUIDModel, HistoryModel, DeletedModel):
    id = models.BigAutoField(primary_key=True)
    team_id = models.CharField(blank=False, max_length=20)
    user_id = models.CharField(blank=False, max_length=20)
    channel_id = models.CharField(blank=False, max_length=20)
    type = models.CharField(max_length=40, choices=MessageType.choices, default=MessageType.MESSAGE)
    subtype = models.CharField(max_length=40, choices=MessageSubType.choices, default=MessageSubType.EMPTY)
    text = models.TextField(default="", max_length=40000)
    metadata = models.JSONField(default=dict)

    created = None
    ts = models.DateTimeField(auto_now_add=True, db_index=True)
    client_msg_id = models.CharField(max_length=50, null=False, default="")

    objects = MessageManager()

    @property
    def timestamp(self) -> int:
        return utils.to_timestamp(self.ts)

    class Meta:
        db_table = "messages"
        ordering = ["-ts"]
