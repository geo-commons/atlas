from django.shortcuts import render, redirect
from constance import config
from homepage.views import _get_config, _get_user
from webservice.models import Selection, Map
from tables.models import Table


def index(request):
    if not config.FEATURE_PORTAL:
        return redirect('/atlas/')

    context = {
        'data': {
            'config': _get_config(request),
            'user': _get_user(request),
            'selections': [map.to_dict() for map in Selection.authorized.for_request(request)],
            'maps': [map.to_dict() for map in Map.authorized.for_request(request)],
            'tables': [table.to_dict() for table in Table.authorized.for_request(request)]
        }
    }

    return render(request, 'portal/index.html', context)
