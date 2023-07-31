import django_filters
from django.db.models import Q
from django import forms
from .models import Dataset, Topic


class DatasetFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(
        lookup_expr='icontains', label='', method='filter_by_multiple_fields')

    topic = django_filters.ModelMultipleChoiceFilter(
        label='Onderwerp', queryset=Topic.objects, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Dataset
        fields = ['q']

    def filter_by_multiple_fields(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(
                abstract__icontains=value)
        )
