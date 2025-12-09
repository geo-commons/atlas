from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from tables_v2.models import TableTemp
from tables_v2.serializers import TableTempSerializer
from webservice.mixins import DataExportImportMixin, DeleteMixin


# TODO: add resource class
class TableTempViewSet(DataExportImportMixin, DeleteMixin, viewsets.ModelViewSet):
    serializer_class = TableTempSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    queryset = TableTemp.objects.all()