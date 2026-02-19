from django.shortcuts import render, redirect
from constance import config
from homepage.views import _get_config, _get_user
from tables.models import Table
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

    tables = Table.authorized.for_request(request).exists()

    return {'maps': maps, 'metadatasets': metadatasets, 'tables': tables}


def index(request, slug=None):
    if not config.FEATURE_PORTAL:
        return redirect('/atlas/')

    context = {
        'data': {
            'config': _get_config(request),
            'user': _get_user(request),
            'portalAvailableLinks': _get_portal_available_links(request),
        }
    }

    return render(request, 'portal/index.html', context)
