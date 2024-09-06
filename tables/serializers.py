from rest_framework import serializers

from tables.models import Table


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['slug', 'source', 'search_fields', 'list_fields', 'endpoint', 'method', 'title', 'list_query',
                  'login_required', 'only_internal', 'ordering', 'created_at', 'updated_at', 'id', 'error_template',
                  'list_headings']