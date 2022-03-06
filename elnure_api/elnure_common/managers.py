from django.db.models import Manager


class ElnureManagerMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs["filter_lookups"] = cls.get_filter_lookups(bases, attrs)
        return super().__new__(cls, name, bases, attrs)

    @classmethod
    def get_filter_lookups(cls, bases, attrs):
        filter_lookups = attrs.get("filter_lookups", {}) or {}
        for base in bases:
            if getattr(base, "filter_lookups", None):
                filter_lookups |= base.filter_lookups
        return filter_lookups


class ElnureManager(Manager, metaclass=ElnureManagerMetaclass):
    filter_lookups = None

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(**self.filter_lookups)


class ActiveManager(ElnureManager):
    filter_lookups = {"active": True}
