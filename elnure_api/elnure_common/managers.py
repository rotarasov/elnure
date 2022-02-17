from django.db.models import Manager


class ElnureManager(Manager):
    filter_lookups = {}

    def __new__(cls):
        for klass in cls.mro()[1:]:
            if issubclass(klass, ElnureManager):
                cls.filter_lookups |= klass.filter_lookups
        return super().__new__(cls)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(**self.filter_lookups)


class ActiveManager(ElnureManager):
    filter_lookups = {"active": True}
