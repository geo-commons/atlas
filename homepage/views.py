import logging

from constance.admin import get_values
from django.http import HttpResponseNotFound
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt

from webservice.models import Layer, Map, Viewer
from .lib import get_help_content


logger = logging.getLogger(__name__)
help_content = get_help_content()


@xframe_options_exempt
def embed(request):
    authorized_layers = Layer.authorized.for_request(request)
    visible_layers = authorized_layers.filter(~Q(not_in_atlas=True))

    context = {
        'data': {
            'is_embed': True,
            'config': _get_config(request),
            'user': _get_user(request),
            'layers': _default_layers() + [layer.to_dict() for layer in visible_layers]
        }
    }

    return render(request, 'v3/app.html', context)


def v3(request, theme_slug=''):
    authorized_layers = Layer.authorized.for_request(request).prefetch_related(
        'layer_source', 'layer_type', 'linked_data', 'templates'
    )

    context = {}

    if theme_slug:
        theme = get_object_or_404(Map, slug=theme_slug)
        visible_layers = authorized_layers.filter(map=theme)
        context['title'] = theme.title
    else:
        visible_layers = authorized_layers.filter(~Q(not_in_atlas=True))

    context['data'] = {
        'is_embed': False,
        'config': _get_config(request),
        'user': _get_user(request),
        'layers': _default_layers() + [layer.to_dict() for layer in visible_layers]
    }

    return render(request, 'v3/app.html', context)


def v3_help(request):
    return render(request, 'v3/help.html', {
        'title': 'Help',
        'content': help_content
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
def v3_admin(request):
    if not request.user.is_superuser:
        return redirect(reverse('admin:login'))

    authorized_layers = Layer.authorized.for_request(request).prefetch_related(
        'layer_source', 'layer_type', 'linked_data', 'templates'
    )
    visible_layers = authorized_layers.filter(~Q(not_in_atlas=True))

    context = {
        'data':  {
            'config': _get_config(request),
            'user': _get_user(request),
            'layers': _default_layers() + [layer.to_dict() for layer in visible_layers]
        }
    }

    return render(request, 'v3/admin.html', context)


@xframe_options_exempt
def v3_map(request, slug):
    authorized_layers = Layer.authorized.for_request(request).prefetch_related(
        'layer_source', 'layer_type', 'linked_data', 'templates'
    )
    visible_layers = authorized_layers.filter(~Q(not_in_atlas=True))
    visible_map = get_object_or_404(
        Map.authorized.for_request(request), slug=slug)

    context = {
        'data': {
            'config': _get_config(request),
            'user': _get_user(request),
            'map': visible_map.to_dict(),
            'layers': _default_layers() + [layer.to_dict() for layer in visible_layers]
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
        'position': {
            'zoom': config.get('POSITION_ZOOM'),
            'center': {
                'x': config.get('POSITION_CENTER_X'),
                'y': config.get('POSITION_CENTER_Y')
            }
        },
        'suggest_municipalities': config.get('SUGGEST_MUNICIPALITIES'),
        'show_disclaimer': config.get('DISCLAIMER') != '',
        'features': {
            'print': config.get('FEATURE_PRINT'),
            'draw': config.get('FEATURE_DRAW'),
            'portal': config.get('FEATURE_PORTAL'),
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
    }
