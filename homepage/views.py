import logging
import os

from constance.admin import get_values
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_sameorigin
from django.views.decorators.csrf import ensure_csrf_cookie

from homepage.templatetags.app_version import app_version
from webservice.models import Layer, Map, Viewer

logger = logging.getLogger(__name__)


@xframe_options_exempt
def embed(request):
    authorized_layers = Layer.authorized.for_request(request).select_related('metadataset')
    visible_layers = authorized_layers.filter(~Q(not_in_atlas=True))
    user = _get_user(request)

    context = {
        'data': {
            'is_embed': True,
            'config': _get_config(request),
            'user': user,
            'layers': _default_layers() + [layer.to_dict(request.user, request) for layer in visible_layers]
        }
    }

    return render(request, 'v3/app.html', context)


@xframe_options_exempt
@ensure_csrf_cookie
def v3(request, theme_slug=''):
    authorized_layers = Layer.authorized.for_request(request).prefetch_related(
        'layer_source', 'layer_type', 'linked_data', 'templates'
    ).select_related('metadataset')
    user = _get_user(request)

    context = {}

    # We set outdated_map_slug to None by default. If the user is on an outdated map (i.e., when theme_slug is set)
    # we update it to that slug. This allows us to later display a message in the frontend
    # letting the user know they are using an old map view, along with a redirect to the new map view.
    outdated_map_slug = None

    if theme_slug:
        theme = get_object_or_404(Map, slug=theme_slug)
        visible_layers = authorized_layers.filter(map=theme)
        outdated_map_slug = theme_slug
        context['title'] = theme.title
    else:
        visible_layers = authorized_layers.filter(~Q(not_in_atlas=True))

    context['data'] = {
        'is_embed': False,
        'config': _get_config(request),
        'user': user,
        'layers': _default_layers() + [layer.to_dict(request.user, request) for layer in visible_layers],
        'outdated_map_slug': outdated_map_slug,
    }

    return render(request, 'v3/app.html', context)


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

    visible_layers = Layer.authorized.for_request(request).prefetch_related(
        'layer_source', 'layer_type', 'linked_data', 'templates'
    )

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


@xframe_options_exempt
def v3_map(request, slug):
    visible_layers = Layer.authorized.for_request(request).prefetch_related(
        'layer_source', 'layer_type', 'linked_data', 'templates'
    )
    visible_map = get_object_or_404(
        Map.authorized.for_request(request), slug=slug)
    user = _get_user(request)

    context = {
        'data': {
            'config': _get_config(request),
            'user': user,
            'map': visible_map.to_dict(),
            'layers': _default_layers() + [layer.to_dict(request.user, request) for layer in visible_layers]
        }
    }

    return render(request, 'v3/map.html', context)


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


def _get_config(request):
    config = get_values()

    return {
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
        'suggest_municipalities': config.get('SUGGEST_MUNICIPALITIES'),
        'show_disclaimer': config.get('DISCLAIMER') != '',
        'features': {
            'print': config.get('FEATURE_PRINT'),
            'draw': config.get('FEATURE_DRAW'),
            'portal': config.get('FEATURE_PORTAL'),
            'edit_layer_features': config.get('FEATURE_EDIT_LAYER_FEATURES'),
            'sortLayer': config.get('FEATURE_SORT_LAYER'),
            'compareLayers': config.get('FEATURE_COMPARE_LAYERS'),
            'newTables': config.get('FEATURE_NEW_TABLES'),
            'oldLinkedDataAndTemplate': config.get('FEATURE_OLD_LINKED_DATA_AND_TEMPLATE')
        },
        'viewers': [viewer.to_dict() for viewer in Viewer.visible.for_request(request)],
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
