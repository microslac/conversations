from django.db.models.manager import BaseManager
from micro.jango.models.history import DeletedManager

from channels.querysets.channel import ChannelQuerySet


class ChannelManager(DeletedManager):
    def filter(self, *args, **kwargs) -> ChannelQuerySet:
        return super().filter(*args, **kwargs)

    def get_queryset(self) -> ChannelQuerySet:
        return ChannelQuerySet(self.model, using=self._db)

    def from_team(self, team_id: str):
        return self.get_queryset().from_team(team_id)
