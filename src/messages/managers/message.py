from core.models.history import DeletedManager, DeletedQuerySet


class MessageQuerySet(DeletedQuerySet):
    pass


class MessageManager(DeletedManager):
    def get_queryset(self):
        return MessageQuerySet(self.model, using=self._db).filter(deleted__isnull=True)

    def include_deleted(self):
        return MessageQuerySet(self.model, using=self._db)
