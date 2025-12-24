import json
from io import BytesIO
from os import path, listdir
from tempfile import TemporaryDirectory
import re
import zipfile

import fiona
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import HttpResponse
from django.views.decorators.http import require_http_methods
from fiona.errors import FionaValueError, DriverError
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


def sanitize_filename(filename, max_length=100):
    """
    Sanitize filename to prevent path traversal and invalid characters.

    - Allows only [a-zA-Z0-9-_]
    - Replaces other characters with '-'
    - Strips leading dots
    - Caps length to max_length
    - Ensures non-empty result
    """
    if not filename:
        return 'output'

    # Replace any character that's not alphanumeric, dash, or underscore with '-'
    sanitized = re.sub(r'[^a-zA-Z0-9_-]', '-', filename)

    # Strip leading dots (prevents hidden files and path issues)
    sanitized = sanitized.lstrip('.')

    # Cap length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]

    # Ensure non-empty result
    if not sanitized:
        return 'output'

    return sanitized


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
        data = {
            'error': f"Invalid output format provided: {output_format}"
        }
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

    temp_dir = TemporaryDirectory()

    # Parse request data
    try:
        request_data = json.loads(request.body.decode('utf-8'))
        raw_filename = request_data.get('filename', 'output')
        filename = sanitize_filename(raw_filename)
        geojson_data = request_data.get('featureCollection', request_data)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        temp_dir.cleanup()
        data = {
            'error': f"Invalid JSON data: {str(e)}"
        }
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

    file_name = f'{filename}{formats[output_format]}'

    # For shapefiles, fiona needs the base filename without extension
    # It will create .shp, .shx, .dbf, etc. files with that base name
    if output_format == 'ESRI Shapefile':
        output_file = path.join(temp_dir.name, filename)
    else:
        output_file = path.join(temp_dir.name, file_name)

    # Process geospatial data
    try:
        geojson_bytes = json.dumps(geojson_data).encode('utf-8')

        with fiona.open(BytesIO(geojson_bytes), driver='GeoJSON') as inputCollection:
            with fiona.open(output_file, 'w', driver=output_format, schema=inputCollection.schema,
                            crs=inputCollection.crs) as outputCollection:
                for feature in inputCollection:
                    outputCollection.write(feature)

        # For shapefiles, zip all the created files (.shp, .shx, .dbf, etc.)
        if output_format == 'ESRI Shapefile':
            zip_path = path.join(temp_dir.name, file_name)
            try:
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    base_name = path.basename(output_file)
                    for file in listdir(temp_dir.name):
                        file_path = path.join(temp_dir.name, file)
                        if path.isfile(file_path) and file.startswith(base_name) and not file.endswith('.zip'):
                            zipf.write(file_path, file)
                output_file = zip_path
            except (zipfile.BadZipFile, OSError, IOError) as e:
                temp_dir.cleanup()
                data = {
                    'error': f"Failed to create zip file: {str(e)}"
                }
                return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except (FionaValueError, DriverError) as e:
        temp_dir.cleanup()
        data = {
            'error': f"Invalid or unsupported geospatial data: {str(e)}"
        }
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        temp_dir.cleanup()
        data = {
            'error': f"Failed to process geospatial file: {str(e)}"
        }
        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Stream file with cleanup in finally
    def file_iterator(file_path, chunk_size=8192):
        try:
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(chunk_size)
                    if not data:
                        break
                    yield data
        finally:
            temp_dir.cleanup()

    response = StreamingHttpResponse(file_iterator(output_file))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    return response
