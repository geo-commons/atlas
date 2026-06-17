import logging
import math
import os
from urllib.parse import urlencode

from constance.admin import get_values
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_sameorigin
from django.views.decorators.csrf import ensure_csrf_cookie
from inertia import render as inertia_render

from homepage.templatetags.app_version import app_version
from webservice.models import Layer, Map, Viewer

logger = logging.getLogger(__name__)


LAYER_PREFETCH_FIELDS = (
    'layer_source',
    'layer_type',
    'layer_type__parent',
    'linked_data',
    'templates',
    'related_tables',
    'related_tables__source',
    'related_tables__tables',
    'related_tables__tables__source',
    'related_tables__outgoing_table_relations',
    'layer_table_relations',
)

ADMIN_ROUTE_DEFINITIONS = (
    ('/', 'Admin/Dashboard', {'title': 'Dashboard', 'menu': True}),
    ('/configuration', 'Admin/Configuration', {'title': 'Configuratie', 'menu': True}),
    ('/portal-configuration', 'Admin/PortalConfiguration', {'title': 'Portaal configuratie', 'menu': True}),
    ('/maps', 'Admin/Maps', {'title': 'Kaarten', 'menu': True}),
    ('/sources', 'Admin/Sources', {'title': 'Bronnen', 'menu': True}),
    ('/layers', 'Admin/Layers', {'title': 'Kaartlagen', 'menu': True}),
    ('/categories', 'Admin/Categories', {'title': 'Categorieën', 'menu': True}),
    ('/tables', 'Admin/Tables', {'title': 'Tabellen', 'menu': True}),
    ('/tables_old', 'Admin/TablesOld', {'title': 'Tabellen (oud)', 'menu': True}),
    ('/users', 'Admin/Users', {'title': 'Gebruikers', 'menu': True}),
    ('/groups', 'Admin/Groups', {'title': 'Groepen', 'menu': True}),
    ('/viewers', 'Admin/Viewers', {'title': 'Viewers', 'menu': True}),
    ('/logs', 'Admin/Logs', {'title': 'Logs', 'menu': True}),
    ('/authorizations', 'Admin/Authorizations', {'title': 'Autorisaties', 'menu': True}),
    ('/metadatasets', 'Admin/Metadatasets', {'title': 'Metadatasets', 'menu': True}),
    ('/general-information', 'Admin/GeneralInformation', {'title': 'Algemene informatie', 'menu': True}),
)

ADMIN_UPDATE_ROUTE_DEFINITIONS = (
    ('/maps/update/', 'Admin/MapUpdate', {'title': 'Kaarten', 'menu': False}),
    ('/sources/update/', 'Admin/SourceUpdate', {'title': 'Bron bewerken', 'menu': True, 'breadcrumb': {'sources': {'title': 'Bronnen'}}}),
    ('/layers/update/', 'Admin/LayerUpdate', {'title': 'Kaartlaag bewerken', 'menu': True, 'breadcrumb': {'layers': {'title': 'Kaartlagen'}}}),
    ('/categories/update/', 'Admin/CategoryUpdate', {'title': 'Categorie bewerken', 'menu': True, 'breadcrumb': {'categories': {'title': 'Categorieën'}}}),
    ('/tables/update/', 'Admin/TableUpdate', {'title': 'Tabel bewerken', 'menu': True, 'breadcrumb': {'tables': {'title': 'Tabellen'}}}),
    ('/tables_old/update/', 'Admin/TableOldUpdate', {'title': 'Tabel (oud) bewerken', 'menu': True, 'breadcrumb': {'tables': {'title': 'Tabellen'}}}),
    ('/users/update/', 'Admin/UserUpdate', {'title': 'Gebruiker bewerken', 'menu': True, 'breadcrumb': {'users': {'title': 'Gebruikers'}}}),
    ('/groups/update/', 'Admin/GroupUpdate', {'title': 'Groep bewerken', 'menu': True, 'breadcrumb': {'groups': {'title': 'Groepen'}}}),
    ('/viewers/update/', 'Admin/ViewerUpdate', {'title': 'Viewer bewerken', 'menu': True, 'breadcrumb': {'viewers': {'title': 'Viewers'}}}),
    ('/logs/update/', 'Admin/LogUpdate', {'title': 'Log Bewerken', 'menu': True, 'breadcrumb': {'viewers': {'title': 'Logs'}}}),
    ('/authorizations/update/', 'Admin/AuthorizationUpdate', {'title': 'Autorisatie bewerken', 'menu': True, 'breadcrumb': {'authorizations': {'title': 'Autorisaties'}}}),
    ('/metadatasets/update/', 'Admin/MetadatasetUpdate', {'title': 'Metadataset Bewerken', 'menu': True, 'breadcrumb': {'metadatasets': {'title': 'Metadatasets'}}}),
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
    
    props = {
        'config': _get_config(request, visible_map),
        'user': user,
        'map': visible_map.to_dict(),
        'layers': _default_layers() + [layer.to_dict(request.user, request) for layer in authorized_layers],
        'route': _get_route_props(request, app='map', path=request.path, base_path=''),
    }

    return inertia_render(request, 'Map', props=props, template_data={
        'title': 'Atlas',
        'vite_entry': 'src/map.js',
    })


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
def v3_admin(request, path=''):
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

    route = _get_admin_route_props(request, path)

    props = {
        'config': config,
        'user': user,
        'layers': _default_layers() + [layer.to_dict(request.user, request) for layer in visible_layers],
        'route': route,
    }

    return inertia_render(request, route['component'], props=props, template_data={
        'title': 'Atlas',
        'vite_entry': 'src/admin.js',
    })


def _get_admin_route_props(request, path):
    normalized_path = f"/{path.strip('/')}" if path else '/'
    if normalized_path != '/' and normalized_path.endswith('/'):
        normalized_path = normalized_path.rstrip('/')

    component = 'Admin/NotFound'
    meta = {'title': 'Niet gevonden', 'menu': False}
    params = {}

    for route_path, route_component, route_meta in ADMIN_ROUTE_DEFINITIONS:
        if normalized_path == route_path:
            component = route_component
            meta = route_meta
            break
    else:
        for route_prefix, route_component, route_meta in ADMIN_UPDATE_ROUTE_DEFINITIONS:
            if normalized_path.startswith(route_prefix):
                route_id = normalized_path.replace(route_prefix, '', 1)
                if route_id and '/' not in route_id:
                    component = route_component
                    meta = route_meta
                    params = {'id': route_id}
                break

    return _get_route_props(
        request,
        app='admin',
        path=normalized_path,
        base_path='/atlas/admin',
        component=component,
        meta=meta,
        params=params,
    )


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


def _get_route_props(request, app, path, base_path, component=None, meta=None, params=None):
    query = {key: request.GET.get(key) for key in request.GET}
    query_string = urlencode(query)

    return {
        'app': app,
        'basePath': base_path,
        'path': path,
        'fullPath': f'{path}?{query_string}' if query_string else path,
        'query': query,
        'params': params or {},
        'meta': meta or {},
        'component': component,
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
