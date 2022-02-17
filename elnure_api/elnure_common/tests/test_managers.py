import pytest

from elnure_common.managers import ElnureManager


def test_manager_lookups():
    CustomManager1 = type(
        "CustomManager1", (ElnureManager,), {"filter_lookups": {"lookup_1": "foo"}}
    )
    CustomManager2 = type(
        "CustomManager2",
        (CustomManager1, ElnureManager),
        {"filter_lookups": {"lookup_2__in": [1, 2, 3]}},
    )

    assert CustomManager1().filter_lookups == {"lookup_1": "foo"}
    assert CustomManager2().filter_lookups == {
        "lookup_1": "foo",
        "lookup_2__in": [1, 2, 3],
    }
