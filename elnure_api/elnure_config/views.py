from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response

from docio.adapters import RunSnapshotDictsAdapter
from elnure_core.models import RunSnapshot
from elnure_config import models, serializers, filters


class ApplicationWindowViewSet(ModelViewSet):
    """
    Application Window view set

    retrieve: Get an application window by given id
    list: Get all application widows
    create: Create an application window
    update: Update an application window by id
    partial_update: Update only some fields of an application window by id
    delete: Delete an application window by id
    formation_results: Get results of elective group formation for this application window
    """

    serializer_class = serializers.ApplicationWindowSerializer
    queryset = models.ApplicationWindow.objects
    filterset_class = filters.ApplicationWindowFilterSet

    @action(detail=True, methods=["get"], url_path="formation-results")
    def formation_results(self, request, pk=None):
        application_window = self.get_object()
        try:
            run_snapshot = application_window.strategy_run_results.filter(
                status=RunSnapshot.Status.ACCEPTED
            ).latest("update_date")
        except RunSnapshot.DoesNotExist:
            return Response([])

        adapter = RunSnapshotDictsAdapter()
        results = adapter.forward(run_snapshot)
        return Response(results)


class RefApplicationWindowViewSet(ListModelMixin, GenericViewSet):
    serializer_class = serializers.RefApplicationWindowSerializer
    queryset = models.ApplicationWindow.objects
    filterset_class = filters.ApplicationWindowFilterSet
