from inertia import render as inertia_render

from homepage.views import _get_config, _get_route_props, _get_user
from .models import Table


def index(request):
    visible_tables = Table.authorized.for_request(request)
    route = _get_tables_route_props(request)

    props = {
        'config': _get_config(request),
        'user': _get_user(request),
        'tables': [table.to_dict() for table in visible_tables],
        'route': route,
    }

    return inertia_render(request, route['component'], props=props, template_data={
        'title': 'Atlas',
        'vite_entry': 'src/tables.js',
    })


def _get_tables_route_props(request):
    path = request.path.removeprefix('/tables-old')
    path = path.rstrip('/') or '/'
    params = {}
    component = 'Tables/NotFound'

    if path != '/':
        table_slug = path.lstrip('/')
        if '/' not in table_slug:
            params = {'tableSlug': table_slug}
            component = 'Tables/List'

    return _get_route_props(
        request,
        app='tables',
        path=path,
        base_path='/tables-old',
        component=component,
        meta={},
        params=params,
    )
