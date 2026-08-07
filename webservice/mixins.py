import sys
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.http import HttpResponse
from django.utils.text import slugify
from rest_framework.decorators import action
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from tablib import Dataset

from authz.models import Authorization
from authz.resources import AuthorizationResource
from tables.models import Table as OldTable
from tables.resources import TableResource as OldTableResource
from webservice.models import Category, Layer, Map, Source, Viewer, Metadataset
from table.models import Table
from .resources import CategoryResource, LayerResource, MapResource, SourceResource, ViewerResource, MetadatasetResource
from table.resources import TableResource
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
        Metadataset: MetadatasetResource,
        Viewer: ViewerResource,
        OldTable: OldTableResource,
        Authorization: AuthorizationResource,
        Table: TableResource
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
        response = HttpResponse(
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
            raise ValidationError({
                'detail': 'File with name file not found'
            }) from exc

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
            # 3 is the alpha channel
            background.paste(img, mask=img.split()[3])
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
            img.save(output, format=image_format,
                     quality=quality, optimize=True)
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
    @transaction.atomic
    def data_duplicate(self, request):
        """
        Duplicate all objects for the submitted ids.
        """
        serializer = DuplicateSettingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ids_to_duplicate = serializer.validated_data.get('ids', [])
        if not ids_to_duplicate:
            raise ValidationError({'detail': 'No objects were selected for duplication.'})

        queryset = self.get_queryset().filter(pk__in=ids_to_duplicate)
        duplicated_ids = set(queryset.values_list('pk', flat=True))
        not_duplicated_ids = sorted(set(ids_to_duplicate) - duplicated_ids)
        if not_duplicated_ids:
            raise ValidationError({
                'detail': 'Some objects could not be duplicated.',
                'ids': not_duplicated_ids,
            })

        for obj in queryset:
            self.duplicate_object(obj)

        return Response({
            'message': 'Successfully duplicated objects',
        }, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def duplicate_object(self, obj):
        """
        Create and save a duplicate of one model instance in a transaction.
        """
        model_class = obj.__class__
        duplicate = model_class.objects.get(pk=obj.pk)
        many_to_many_values = self.get_many_to_many_values(duplicate)

        self.prepare_duplicate(duplicate)
        duplicate.save()
        self.set_many_to_many_values(duplicate, many_to_many_values)
        self.after_duplicate(obj, duplicate)

        return duplicate

    def prepare_duplicate(self, duplicate):
        """
        Reset identity fields and assign duplicate names before saving.
        """
        model_class = duplicate.__class__
        duplicate.pk = None

        duplicate_name_field = self.get_duplicate_name_field(duplicate)
        if not duplicate_name_field:
            return duplicate

        original_name = getattr(duplicate, duplicate_name_field)
        new_name = self.get_unique_duplicate_name(model_class, duplicate_name_field, original_name)
        setattr(duplicate, duplicate_name_field, new_name)

        if hasattr(duplicate, 'slug'):
            duplicate.slug = self.get_unique_slug(model_class, slugify(new_name))

        return duplicate

    def get_duplicate_name_field(self, obj):
        """
        Return the field used to create a human-readable duplicate name.
        """
        if hasattr(obj, 'title'):
            return 'title'

        if hasattr(obj, 'label'):
            return 'label'

        return None

    def get_unique_duplicate_name(self, model_class, field_name, value):
        """
        Build a unique duplicate name using the "Name (2)" pattern.
        """
        i = 2
        while model_class.objects.filter(**{field_name: f'{value} ({i})'}).exists():
            i += 1

        return f'{value} ({i})'

    def get_unique_slug(self, model_class, base_slug):
        """
        Build a unique slug from a candidate slug value.
        """
        slug = base_slug
        i = 2

        while model_class.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{i}'
            i += 1

        return slug

    def get_many_to_many_values(self, obj):
        """
        Collect many-to-many values before the duplicate is saved.
        """
        return {
            field.name: list(getattr(obj, field.name).all())
            for field in obj._meta.many_to_many
            if field.remote_field.through._meta.auto_created
        }

    def set_many_to_many_values(self, obj, values):
        """
        Restore many-to-many values on the saved duplicate.
        """
        for field_name, field_values in values.items():
            getattr(obj, field_name).set(field_values)

    def after_duplicate(self, _obj, _duplicate):
        """
        Hook for viewsets that need to copy extra relations after saving.
        """
        pass


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
