from django.db.models import F, Q
from rest_framework import filters


class NullsLastTimestampOrderingFilter(filters.OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if not ordering:
            return queryset

        ordered_fields = []
        for field in ordering:
            field_name = field.removeprefix('-')
            if field_name not in {'created_at', 'updated_at'}:
                ordered_fields.append(field)
            elif field.startswith('-'):
                ordered_fields.append(F(field_name).desc(nulls_last=True))
            else:
                ordered_fields.append(F(field_name).asc(nulls_last=True))

        return queryset.order_by(*ordered_fields)


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
