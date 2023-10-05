from io import BytesIO
from os import path
from tempfile import TemporaryDirectory

from django.core.exceptions import ValidationError
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import HttpResponse
from django.views.decorators.http import require_http_methods
import fiona
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Source
from .authorization import can_request_access_source, authorize_ows_request, authorize_wmts_request


def v3_token(request):
    if request.user.is_authenticated:
        refresh = RefreshToken.for_user(request.user)

        return JsonResponse({
            'token': str(refresh.access_token)
        })

    return HttpResponse('Unauthorized', status=401)


def v3_authorize(request):
    source_slug = request.headers.get('X-Source-Slug')
    if not source_slug:
        return JsonResponse({
            'allow': False,
            'message': 'The header X-Source-Slug is not defined'
        }, status=400)

    try:
        source = Source.objects.get(slug=source_slug)
    except Source.DoesNotExist:
        return JsonResponse({
            'allow': False,
            'message': f'could not find source with slug {source_slug}'
        }, status=400)

    if not can_request_access_source(request, source):
        return JsonResponse({
            'allow': False,
            'message': f'user does not have access to source {source_slug}'
        }, status=403 if request.user.is_authenticated else 401)

    result = False
    if source.source_type == Source.SOURCE_OWS:
        result = authorize_ows_request(request, source)
    elif source.source_type == Source.SOURCE_WMTS:
        result = authorize_wmts_request(request, source)
    elif source.source_type == Source.SOURCE_REST:
        result = True  # REST authentication is performed on source level

    if result:
        return JsonResponse({
            'allow': True,
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'name': request.user.name,
                'groups': [
                    g.slug for g in request.user.atlas_groups.filter(slug__isnull=False)
                ]
            } if request.user.is_authenticated else None
        })

    return JsonResponse({
        'allow': False,
        'message': f'user does not have access to layer of source {source_slug}'
    }, status=403 if request.user.is_authenticated else 401)


@require_http_methods(['POST'])
def v3_convert(request, output_format):
    formats = {
        'ESRI Shapefile': '.shp.zip',
        'GeoJSON': '.geojson',
        'GPKG': '.gpkg',
        'GML': '.gml',
        'SQLite': '.sqlite3'
    }

    if output_format not in formats:
        raise ValidationError(
            f"Invalid output format provided: {output_format}"
        )

    file_name = f'output{formats[output_format]}'

    temp_dir = TemporaryDirectory()  # pylint: disable=consider-using-with
    output_file = path.join(temp_dir.name, file_name)

    with fiona.open(BytesIO(request.body), driver='GeoJSON') as inputCollection:
        # GeoJSON, ESRI Shapefile, GPKG, SQLite, GML
        with fiona.open(output_file, 'w', driver=output_format, schema=inputCollection.schema, crs=inputCollection.crs) as outputCollection:
            for feature in inputCollection:
                outputCollection.write(feature)

    def file_iterator(file_path, chunk_size=8192):
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                yield data

        temp_dir.cleanup()

    response = StreamingHttpResponse(file_iterator(output_file))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    return response
