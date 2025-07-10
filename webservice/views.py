import json
from io import BytesIO
from os import path
from tempfile import TemporaryDirectory

import fiona
from django.core.exceptions import ValidationError
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import HttpResponse
from django.views.decorators.http import require_http_methods
from rest_framework_simplejwt.tokens import RefreshToken


def v3_token(request):
    if request.user.is_authenticated:
        refresh = RefreshToken.for_user(request.user)

        return JsonResponse({
            'token': str(refresh.access_token)
        })

    return HttpResponse('Unauthorized', status=401)


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

    temp_dir = TemporaryDirectory()
    output_file = path.join(temp_dir.name, file_name)

    try:
        request_data = json.loads(request.body.decode('utf-8'))
        geojson_data = request_data.get('featureCollection', request_data)
        geojson_bytes = json.dumps(geojson_data).encode('utf-8')

    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise ValidationError(f"Invalid JSON data: {str(e)}") from e

    with fiona.open(BytesIO(geojson_bytes), driver='GeoJSON') as inputCollection:
        # GeoJSON, ESRI Shapefile, GPKG, SQLite, GML
        with fiona.open(output_file, 'w', driver=output_format, schema=inputCollection.schema,
                        crs=inputCollection.crs) as outputCollection:
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
