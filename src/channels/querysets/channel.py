import re
from typing import TYPE_CHECKING

from django.db.models import QuerySet

from core.models.history import DeletedQuerySet

if TYPE_CHECKING:
    from channels.models import Channel


class ChannelQuerySet(DeletedQuerySet):
    def filter(self, *args, **kwargs) -> QuerySet["Channel"]:
        return super().filter(*args, **kwargs)

    def create(self, **kwargs) -> "Channel":
        return super().create(**kwargs)

    def from_team(self, team_id: str):
        return self.filter(team_id=team_id)

    def general_channels(self):
        return self.filter(is_general=True)

    def archived_channels(self):
        return self.filter(is_archived=True)

    def private_channels(self):
        return self.filter(is_private=True)

    def shared_channels(self):
        return self.filter(is_shared=True)

    def channels(self):
        return self.filter(is_channel=True)

    def ims(self):
        return self.filter(is_im=True)

    def mpims(self):
        return self.filter(mpim=True)


class ChChannelQuerySet(ChannelQuerySet):
    def create(self, **kwargs) -> "Channel":
        kwargs.update(is_channel=True, is_im=False, is_mpim=False)
        return super().create(**kwargs)


class ImChannelQuerySet(ChannelQuerySet):
    def create(self, **kwargs) -> "Channel":
        cid: str = self.model.id.field.get_default()
        im_id = re.sub(r"^\w", "D", cid)
        kwargs.update(is_im=True, is_channel=False, is_mpim=False, id=im_id)
        return super().create(**kwargs)


class MpimChannelQuerySet(ChannelQuerySet):
    def create(self, **kwargs) -> "Channel":
        cid: str = self.model.id.field.get_default()
        mpim_id = re.sub(r"^\w", "G", cid)
        kwargs.update(s_mpim=True, is_channel=False, is_im=False, id=mpim_id)
        return super().create(**kwargs)
