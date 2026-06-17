from constance import config
from django.shortcuts import redirect
from inertia import render as inertia_render

from homepage.views import _get_config, _get_route_props, _get_user
from table.models import Table
from webservice.models import Map, Metadataset


def _get_portal_available_links(request):
    """Determine which portal nav links (maps, metadatasets, tables) to show.
    Mirrors the logic from App.vue loadPortalAvailableLinks to avoid 3 API calls per page load.
    Only show links when there is content the user can actually view.
    """
    maps_qs = Map.authorized.for_request(request).filter(published=True, show_in_overview=True)
    if request.user.is_anonymous:
        maps_qs = maps_qs.filter(login_required=False)
    maps = maps_qs.exists()

    if request.user.is_anonymous:
        metadatasets = Metadataset.authorized.for_request(request).filter(show_in_overview=True).exists()
    else:
        metadatasets = Metadataset.authorized.for_request(request).exists()

    tables = Table.authorized.for_request(request).filter(show_in_portal=True).exists()

    return {'maps': maps, 'metadatasets': metadatasets, 'tables': tables}


def index(request, slug=None):
    if not config.FEATURE_PORTAL:
        return redirect('/atlas/')

    route = _get_portal_route_props(request, slug)
    props = {
        'config': _get_config(request),
        'user': _get_user(request),
        'portalAvailableLinks': _get_portal_available_links(request),
        'route': route,
    }

    return inertia_render(request, route['component'], props=props, template_data={
        'title': 'Atlas',
        'vite_entry': 'src/portal.js',
    })


def _get_portal_route_props(request, slug):
    url_name = request.resolver_match.url_name
    route_config = {
        'portal_index': ('/', 'Portal/Dashboard', {'breadcrumb': 'Home', 'menu': False}, {}),
        'portal_maps': ('/maps', 'Portal/Maps', {'breadcrumb': 'Kaarten', 'menu': True}, {}),
        'portal_tables': ('/tables', 'Portal/Tables', {'breadcrumb': 'Tabellen', 'menu': True}, {}),
        'portal_table_detail': (
            f'/tables/{slug}',
            'Portal/TableDetail',
            {'breadcrumb': 'Tabel', 'menu': True, 'parentName': 'Tabellen'},
            {'slug': slug},
        ),
        'portal_search': ('/search', 'Portal/Search', {'breadcrumb': 'Zoeken', 'menu': True}, {}),
        'portal_metadatasets': (
            '/metadatasets',
            'Portal/Metadatasets',
            {'breadcrumb': 'Metadatasets', 'menu': True},
            {},
        ),
        'portal_metadataset_detail': (
            f'/metadatasets/{slug}',
            'Portal/MetadatasetDetail',
            {'breadcrumb': 'Metadataset details', 'menu': True, 'parentName': 'Metadatasets'},
            {'slug': slug},
        ),
    }
    path, component, meta, params = route_config.get(
        url_name,
        (request.path, 'Portal/NotFound', {'breadcrumb': 'Niet gevonden', 'menu': False}, {}),
    )

    return _get_route_props(
        request,
        app='portal',
        path=path,
        base_path='',
        component=component,
        meta=meta,
        params=params,
    )
