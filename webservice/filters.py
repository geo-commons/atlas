import django_filters

from webservice.models import Dataset


class DatasetFilter(django_filters.FilterSet):
    theme_id = django_filters.NumberFilter(field_name='themes__id', lookup_expr='exact')

    class Meta:
        model = Dataset
        fields = ['theme_id']