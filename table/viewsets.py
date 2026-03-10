from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAdminUser

from table.models import Table
from table.serializers import TableSerializer
from webservice.mixins import DataExportImportMixin, DeleteMixin, DuplicateMixin


class TableViewSet(DataExportImportMixin, DuplicateMixin, DeleteMixin, viewsets.ModelViewSet):
    serializer_class = TableSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    filterset_fields = ['show_in_portal']
    
    def get_queryset(self):
        return Table.authorized.for_request(self.request)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_field_value = self.kwargs.get('pk')

        # first check if the lookup field is a slug
        obj = queryset.filter(slug=lookup_field_value).first()

        # if not, check if the lookup field is a primary key
        if obj is None and lookup_field_value.isdigit():
            obj = queryset.filter(pk=lookup_field_value).first()

        # if not, raise an error
        if obj is None:
            raise NotFound(f"No Table matches the given query: {lookup_field_value}")

        return obj

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]