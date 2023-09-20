from django.shortcuts import render
from homepage.views import _get_config, _get_user
from .models import Table


def index(request):
    visible_tables = Table.authorized.for_request(request)

    context = {
        'data': {
            'config': _get_config(request),
            'user': _get_user(request),
            'tables': [table.to_dict() for table in visible_tables]
        }
    }

    return render(request, 'tables/index.html', context)
