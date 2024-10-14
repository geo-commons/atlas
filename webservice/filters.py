import django_filters
from django.db.models import Q
from rest_framework import filters

from webservice.models import Dataset


class DatasetFilter(django_filters.FilterSet):
    theme_id = django_filters.NumberFilter(field_name='themes__id', lookup_expr='exact')

    class Meta:
        model = Dataset
        fields = ['theme_id']


class MultipleFieldsFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_fields = getattr(view, 'multiple_lookup_fields', [])

        for field in filter_fields:
            value = request.query_params.get(field)
            if value:
                values = [v.strip() for v in value.split(',') if v.strip()]
                if values:
                    filters = Q()
                    for v in values:
                        filters |= Q(**{f"{field}": v})
                    queryset = queryset.filter(filters)

        return queryset
