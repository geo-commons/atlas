import sys
from io import BytesIO

from PIL import Image
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.utils.text import slugify
from rest_framework.decorators import action
from rest_framework import permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from tablib import Dataset

from authz.models import Authorization
from authz.resources import AuthorizationResource
from tables.models import Table
from tables.resources import TableResource
from webservice.models import Category, Layer, Map, Source, Theme, Viewer, Dataset as Datasets
from .resources import CategoryResource, LayerResource, MapResource, SourceResource, ThemeResource, ViewerResource, \
    DatasetResource
from .serializers import DataExportSettingsSerializer, DuplicateSettingsSerializer, DeleteSettingsSerializer


class ResourceMappingMixin:
    """
    Mixin to provide a mapping between models and resources.
    """
    model_resource_mapping = {
        Layer: LayerResource,
        Source: SourceResource,
        Map: MapResource,
        Category: CategoryResource,
        Theme: ThemeResource,
        Datasets: DatasetResource,
        Viewer: ViewerResource,
        Table: TableResource,
        Authorization: AuthorizationResource
    }

    def get_resource_class(self):
        """
        Returns the corresponding resource class for the serializer's model.
        """
        model_class = self.serializer_class.Meta.model
        return self.model_resource_mapping.get(model_class)


class DataExportImportMixin(ResourceMappingMixin):
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
        response = HttpResponse(  # pylint: disable=http-response-with-content-type-json
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


class FileUploadMixin(ResourceMappingMixin):
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser], permission_classes=[permissions.IsAdminUser])
    def upload_thumbnail(self, request, pk=None):
        """
        Uploads a thumbnail to an object dynamically, based on the resource mapping.
        """

        resource_class = self.get_resource_class()
        if not resource_class:
            return Response({'error': 'Unable to determine resource class.'}, status=status.HTTP_400_BAD_REQUEST)

        model_class = resource_class._meta.model
        if not model_class:
            return Response({'error': 'Unable to determine model type from resource.'},
                            status=status.HTTP_400_BAD_REQUEST)

        obj_instance = self.get_object()

        if not hasattr(obj_instance, 'thumbnail'):
            return Response({'error': f'{model_class.__name__} does not support thumbnail uploads.'},
                            status=status.HTTP_400_BAD_REQUEST)

        file = request.data.get('file')
        if file:
            resized_image = self.resize_image(file)

            obj_instance.thumbnail = resized_image
            obj_instance.save()
            return Response({'status': f'Thumbnail uploaded successfully to {model_class.__name__} with id {pk}!'},
                            status=status.HTTP_200_OK)

        return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAdminUser])
    def delete_thumbnail(self, _request, pk=None):
        """
        Deletes the thumbnail of an object dynamically.
        """

        resource_class = self.get_resource_class()
        if not resource_class:
            return Response({'error': 'Unable to determine resource class.'}, status=status.HTTP_400_BAD_REQUEST)

        model_class = resource_class._meta.model
        if not model_class:
            return Response({'error': 'Unable to determine model type from resource.'},
                            status=status.HTTP_400_BAD_REQUEST)

        obj_instance = self.get_object()

        if not hasattr(obj_instance, 'thumbnail'):
            return Response({'error': f'{model_class.__name__} does not support thumbnails.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not obj_instance.thumbnail:
            return Response({'error': 'No thumbnail to delete.'}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the thumbnail
        obj_instance.thumbnail.delete(save=True)
        return Response({'status': f'Thumbnail deleted from {model_class.__name__} with id {pk}!'},
                        status=status.HTTP_200_OK)

    def resize_image(self, image_file, max_width=1000, image_format='JPEG', quality=85):
        """
        Resize an uploaded image that's already cropped to 4:3 aspect ratio.
        Just focuses on reducing the size while maintaining the aspect ratio.

        Args:
            image_file: The uploaded file (already cropped to 4:3)
            max_width: Maximum width for the image
            image_format: Output format (JPEG, PNG, etc.)
            quality: Image quality (0-100, JPEG only)

        Returns:
            An InMemoryUploadedFile of the resized image
        """
        # Open the uploaded image
        img = Image.open(image_file)

        # Convert to RGB if the image has an alpha channel (for JPEG format)
        if img.mode in ('RGBA', 'LA') and image_format == 'JPEG':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
            img = background

        # Check aspect ratio (with small tolerance)
        width, height = img.size
        current_ratio = width / height
        target_ratio = 4 / 3

        # Add a small validation that the image is actually 4:3 (with tolerance)
        if abs(current_ratio - target_ratio) > 0.01:
            # The image isn't 4:3, but we'll just resize it as is
            # You could add logging here if needed
            pass

        # Resize the image if it's larger than max_width
        if width > max_width:
            # Calculate new height based on the same aspect ratio
            new_width = max_width
            new_height = int(new_width * height / width)
            img = img.resize((new_width, new_height), Image.LANCZOS)

        # Save the resized image to a BytesIO buffer
        output = BytesIO()

        # Save with appropriate format
        if image_format.upper() == 'JPEG':
            img.save(output, format=image_format, quality=quality, optimize=True)
        else:
            img.save(output, format=image_format, optimize=True)

        output.seek(0)

        # Create a new Django file from the buffer
        return InMemoryUploadedFile(
            output,
            'ImageField',
            f"{image_file.name.split('.')[0]}.{image_format.lower()}",
            f'image/{image_format.lower()}',
            sys.getsizeof(output),
            None
        )


class DuplicateMixin:
    @action(methods=['post'], url_path='duplicate', detail=False, permission_classes=[permissions.IsAdminUser])
    def data_duplicate(self, request):
        serializer = DuplicateSettingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        model_class = self.get_queryset().model
        ids_to_duplicate = serializer.data.get('ids', [])
        queryset = self.get_queryset().filter(pk__in=ids_to_duplicate)

        for obj in queryset:
            duplicate = model_class.objects.get(pk=obj.pk)
            duplicate.pk = None

            # Handle title and slug uniqueness if the model has a title field
            if hasattr(duplicate, 'title'):
                i = 2
                while model_class.objects.filter(title=f'{duplicate.title} ({i})').count() > 0:
                    i += 1

                new_title = f'{duplicate.title} ({i})'
                duplicate.title = new_title

                if hasattr(duplicate, 'slug'):
                    duplicate.slug = slugify(new_title)

            duplicate.save()

        return Response({
            'message': 'Successfully duplicated objects',
        }, status=status.HTTP_201_CREATED)


class DeleteMixin:
    @action(methods=['post'], url_path='delete', detail=False, permission_classes=[permissions.IsAdminUser])
    def data_delete(self, request):
        serializer = DeleteSettingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ids_to_delete = serializer.data.get('ids', [])
        model_class = self.get_queryset().model

        model_class.objects.filter(id__in=ids_to_delete).delete()

        return Response({
            'message': 'Successfully deleted objects',
        }, status=status.HTTP_200_OK)