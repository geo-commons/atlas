from django.shortcuts import render, redirect
from constance import config
from homepage.views import _get_config, _get_user
from tables.models import Table


def index(request, slug=None):
    if not config.FEATURE_PORTAL:
        return redirect('/atlas/')

    context = {
        'data': {
            'config': _get_config(request),
            'user': _get_user(request),
            'tables': [table.to_dict() for table in Table.authorized.for_request(request)],
        }
    }

    return render(request, 'portal/index.html', context)
