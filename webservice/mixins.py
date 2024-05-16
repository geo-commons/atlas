from django.http import HttpResponse
from django.core.exceptions import ValidationError
from tablib import Dataset
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions

from webservice.models import Category, Layer, Map, Source
from .resources import CategoryResource, LayerResource, MapResource, SourceResource
from .serializers import DataExportSettingsSerializer


class DataExportImportMixin:
    model_resource_mapping = {
        Layer: LayerResource,
        Source: SourceResource,
        Map: MapResource,
        Category: CategoryResource
    }

    def get_resource_class(self):
        model_class = self.serializer_class.Meta.model
        return self.model_resource_mapping.get(model_class)


    @action(methods=['post'], url_path='export', detail=False, permission_classes=[permissions.IsAdminUser])
    def data_export(self, request):

        serializer = DataExportSettingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        queryset = self.get_queryset()
        if serializer.data.get('ids') and len(serializer.data['ids']) > 0:
            queryset = queryset.filter(id__in=serializer.data['ids'])

        resource_class = self.get_resource_class()
        resource = resource_class()
        dataset = resource.export(queryset=queryset)

        # We cannot use JSONResponse, as the output of dataset.export is already serialized to JSON
        response = HttpResponse( # pylint: disable=http-response-with-content-type-json
            dataset.export('json'),
            content_type='application/json'
        )

        # note: currently the file name is set in the frontend
        response['Content-Disposition'] = 'attachment; filename=export.json'
        return response

    @action(methods=['post'], url_path='import', detail=False, permission_classes=[permissions.IsAdminUser])
    def data_import(self, request):
        try:
            raw_file = request.FILES['file']
        except KeyError as exc:
            raise ValidationError('File with name file not found') from exc

        dataset = Dataset().load(raw_file.read())

        resource_class = self.get_resource_class()
        resource = resource_class()
        result = resource.import_data(
            dataset=dataset,
            dry_run=request.GET.get('dry_run') == '1'
        )

        print(result)
        print(result.has_errors())
        
        for row in result.rows:
            print(row)

        content = {
            'total_rows': result.total_rows,
            'has_errors': result.has_errors(),
            'rows': [{
                'object_id': row.object_id,
                'import_type': row.import_type,
                'diff': row.diff,
                'errors': [{
                    'error': str(e.error)
                } for e in row.errors]
            } for row in result.rows]
        }

        return Response(content)
