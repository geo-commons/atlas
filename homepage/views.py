import logging
import math
import os

from constance.admin import get_values
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_sameorigin
from django.views.decorators.csrf import ensure_csrf_cookie

from homepage.templatetags.app_version import app_version
from webservice.models import Layer, Map, Viewer

logger = logging.getLogger(__name__)


LAYER_PREFETCH_FIELDS = (
    'layer_source',
    'layer_type',
    'linked_data',
    'templates',
    'related_tables',
    'related_tables__source',
    'related_tables__tables',
    'related_tables__tables__source',
    'related_tables__outgoing_table_relations',
    'layer_table_relations',
)


@xframe_options_exempt
@ensure_csrf_cookie
def v3(request, slug=None):
    authorized_layers = _layers_with_prefetch(request).select_related('metadataset')
    user = _get_user(request)
    
    if slug:
        visible_map = get_object_or_404(
            Map.authorized.for_request(request), slug=slug)
    else:
        visible_map = get_object_or_404(Map.authorized.for_request(request), is_main=True)
    
    context = {
        'data': {
            'config': _get_config(request, visible_map),
            'user': user,
            'map': visible_map.to_dict(),
            'layers': _default_layers() + [layer.to_dict(request.user, request) for layer in authorized_layers]
        }
    }

    return render(request, 'v3/map.html', context)


def v3_disclaimer(request):
    config = get_values()

    if config.get('DISCLAIMER'):
        return render(request, 'v3/disclaimer.html', {
            'title': 'Disclaimer',
            'content': config.get('DISCLAIMER'),
        })

    return HttpResponseNotFound('Er is geen disclaimer aanwezig')


def v3_login(request):
    return render(request, 'v3/login.html', {
        'title': 'Login'
    })


def v3_login_failure(request):
    return render(request, 'v3/login_failure.html', {
        'title': 'Login mislukt'
    })


@login_required(login_url='admin:login')
@ensure_csrf_cookie
@xframe_options_sameorigin
def v3_admin(request):
    user = _get_user(request)

    if not request.user.is_superuser:
        return redirect(reverse('admin:login'))

    visible_layers = _layers_with_prefetch(request)

    config = _get_config(request)
    config = {
        **config,
        'application_version': app_version(),
        'application_environment': os.getenv('ENVIRONMENT'),
    }

    context = {
        'data': {
            'config': config,
            'user': user,
            'layers': _default_layers() + [layer.to_dict(request.user, request) for layer in visible_layers]
        }
    }

    return render(request, 'v3/admin.html', context)


def _default_layers():
    if Layer.objects.filter(is_base=True).count() > 0:
        # Do not return default base layers when the database contains base layers
        return []

    # TODO: Remove default hardcoded layers
    return [
        {
            'id': 'brt_topo_kaart_totaal',
            'title': 'Kaart grijs',
            'name': 'topp:topografische_kaart_grijs',
            'opacity': 0.9,
            'url': 'https://datalab.purmerend.nl/geoserver/topp/wms',
            'server_type': 'geoserver',
            'is_base': True,
            'is_visible': True,
            'metadata': {
                'description': 'Topografische achtergrondkaart',
                'organization': 'Gemeente Purmerend',
                'updated': '2020'
            }
        },
        {
            'id': 'purm_lufo2020',
            'title': 'Luchtfoto 2020',
            'name': 'topp:Lufo_Totaal_2020',
            'opacity': 0.9,
            'url': 'https://datalab.purmerend.nl/geoserver/topp/wms',
            'server_type': 'geoserver',
            'is_base': True,
            'is_visible': False,
            'metadata': {
                'description': 'Luchtfoto',
                'organization': 'Gemeente Purmerend',
                'updated': '2020'
            }
        },
    ]


def _layers_with_prefetch(request):
    return Layer.authorized.for_request(request).prefetch_related(*LAYER_PREFETCH_FIELDS)


def _get_config(request, visible_map=None):
    config = get_values()

    result = {
        'organization_name': config.get('ORGANIZATION_NAME'),
        'organization_logo': settings.MEDIA_URL + config.get('ORGANIZATION_LOGO') if config.get(
            'ORGANIZATION_LOGO') else None,
        'organization_image': settings.MEDIA_URL + config.get('ORGANIZATION_IMAGE') if config.get(
            'ORGANIZATION_IMAGE') else None,
        'organization_primary_color': config.get('ORGANIZATION_PRIMARY_COLOR'),
        'organization_title_color': config.get('ORGANIZATION_TITLE_COLOR'),
        'organization_text_color': config.get('ORGANIZATION_TEXT_COLOR'),
        'organization_introduction': config.get('ORGANIZATION_INTRODUCTION'),
        'organization_header': config.get('ORGANIZATION_HEADER'),
        'position': {
            'zoom': config.get('POSITION_ZOOM'),
            'center': {
                'x': config.get('POSITION_CENTER_X'),
                'y': config.get('POSITION_CENTER_Y')
            }
        },
        'map_area': config.get('MAP_AREA'),
        'suggest_municipalities_brk': config.get('SUGGEST_MUNICIPALITIES_BRK'),
        'suggest_municipalities_bag': config.get('SUGGEST_MUNICIPALITIES_BAG'),
        'show_disclaimer': config.get('DISCLAIMER') != '',
        'features': {
            'print': config.get('FEATURE_PRINT'),
            'portal': config.get('FEATURE_PORTAL'),
            'sortLayer': config.get('FEATURE_SORT_LAYER'),
            'newTables': config.get('FEATURE_NEW_TABLES'),
            'oldLinkedDataAndTemplate': config.get('FEATURE_OLD_LINKED_DATA_AND_TEMPLATE'),
            'featureLayerInternalVisibility': config.get('FEATURE_LAYER_INTERNAL_VISIBILITY'),
        },
        'viewers': [viewer.to_dict() for viewer in Viewer.visible.for_request(request)],
    }
    
    map_position = _normalize_position((visible_map.settings or {}).get('position')) if visible_map else None

    if map_position:
        result['position'] = map_position
        
    return result


def _normalize_position(position):
    try:
        zoom = float(position['zoom'])
        center_x = float(position['center']['x'])
        center_y = float(position['center']['y'])
    except (KeyError, TypeError, ValueError):
        return None

    if not all(math.isfinite(value) for value in (zoom, center_x, center_y)):
        return None

    return {
        'zoom': zoom,
        'center': {
            'x': center_x,
            'y': center_y,
        }
    }


def _get_user(request):
    user = request.user

    if not user.is_authenticated:
        return None

    return {
        'id': user.id,
        'username': user.username,
        'name': user.name,
        'is_authenticated': user.is_authenticated,
        'is_superuser': bool(user.is_authenticated and user.is_superuser),
    }
