from io import BytesIO
from os import path
from tempfile import TemporaryDirectory

from django.core.exceptions import ValidationError
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import HttpResponse
from django.views.decorators.http import require_http_methods
import json
from json import JSONDecodeError
import fiona
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Source
from authz.lib import can_access_source, authorize_ows_request, authorize_wmts_request, authorize_rest_request


def v3_token(request):
    if request.user.is_authenticated:
        refresh = RefreshToken.for_user(request.user)

        return JsonResponse({
            'token': str(refresh.access_token)
        })

    return HttpResponse('Unauthorized', status=401)


def v3_authorize(request):
    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return JsonResponse({
            'result': False,
            'status': 400,
            'message': 'unable to decode json request body'
        }, status=400)

    source_slug = data.get('source')
    if not source_slug:
        return JsonResponse({
            'result': False,
            'status': 400,
            'message': 'source is not defined'
        }, status=400)

    try:
        source = Source.objects.get(slug=source_slug)
    except Source.DoesNotExist:
        return JsonResponse({
            'result': False,
            'status': 400,
            'message': f'could not find source with slug {source_slug}'
        }, status=400)

    if not can_access_source(request, source):
        return JsonResponse({
            'result': False,
            'status': 403 if request.user.is_authenticated else 401,
            'message': f'user {request.user} does not have access to source {source_slug}'
        }, status=403 if request.user.is_authenticated else 401)

    if source.source_type == Source.SOURCE_OWS:
        return authorize_ows_request(source, request, data)
    if source.source_type == Source.SOURCE_WMTS:
        return authorize_wmts_request(source, request, data)
    if source.source_type == Source.SOURCE_REST:
        return authorize_rest_request(source, request, data)

    return JsonResponse({
        'result': False,
        'status': 500,
        'message': 'there is no authorizer for this source type provided'
    })


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
