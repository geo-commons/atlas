import csv
import json
from datetime import datetime
import logging

import requests
from constance import config
from django.conf import settings
from django.http import JsonResponse, HttpResponseNotFound
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from utils.tools import is_ctrix
from webservice.models import Layer, Theme

from .forms import UploadDatasetForm
from .lib import get_help_content
from .models import SavedDataset
from webservice.models import Map, Viewer


logger = logging.getLogger(__name__)
help_content = get_help_content()

class HomePageView(TemplateView):
    template_name = "main_content.html"

    def get_context_data(self, **kwargs):
        user = self.request.user

        context = super().get_context_data(**kwargs)
        context['layers'] = Layer.authorized.user_or_group(user, is_ctrix(self.request)).filter(~Q(not_in_atlas=True))

        context['data'] = {
            'config': _get_config(self.request),
            'user': _get_user(self.request),
            'layers': _default_layers() + [ layer.to_dict() for layer in context['layers'] ]
        }

        return context


WFS_PARAMS = {
    'service': 'wfs',
    'version': 1.0,
    'request': 'GetFeature',
    'typeName': '{}',
    'outputFormat': 'application/json',
    'srsname': 'EPSG:28992'
}


class HandleidingView(TemplateView):
    template_name = 'handleiding.html'


class DownloadsView(ListView):
    # TODO: filtering
    paginate_by = 10
    model = SavedDataset
    template_name = 'downloads.html'


class SavedDatasetView(FormView):
    template_name = 'downloads.html'
    form_class = UploadDatasetForm
    success_url = reversed('homepage:downloads')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            dataset = SavedDataset()
            timestamp = datetime.now().strftime('%Y%m%d%H%M')
            dataset.title = f"{timestamp}-{form.cleaned_data['title']}"
            dataset.json = form.cleaned_data['json']
            if request.user.is_authenticated:
                dataset.saved_by = request.user
            dataset.save()
            logger.debug('dataset %s saved', dataset.title)

        return redirect(reverse('homepage:downloads'))


def save_dataset_view(request, pk, type_):
    dataset = SavedDataset.objects.get(pk=pk)

    if type_ == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f"attachment; filename=\"{dataset.title}.csv\""

        data = dataset.json['features']
        headers = data[0]['properties'].keys()
        writer = csv.DictWriter(response, fieldnames=headers, delimiter=';')
        writer.writeheader()

        for row in data:
            writer.writerow(row['properties'])

        logger.info('downloading csv: %s', dataset.title)
    if type_ == 'json':
        response = JsonResponse(dataset.json)
        logger.info('downloading json: %s', dataset.title)

    return response


def search_wfs(request):
    template_name = 'search_wfs.html'

    query = request.GET.get('q', '')
    layer_id = request.GET.get('layer', '')

    cql_filter = "({} ILIKE '%{}%')"
    filter_list = []
    results = []

    if query and layer_id:
        layer = Layer.objects.get(layer_id=layer_id)
        search_fields = layer._search_fields #pylint: disable=protected-access
        WFS_PARAMS['typeName'] = layer.layer_name

        if search_fields:
            for field in search_fields.split():
                filter_list.append(cql_filter.format(field, query))

            cql_filter = ' or '.join(filter_list)
            WFS_PARAMS['CQL_FILTER'] = cql_filter

            r = requests.get(settings.WFS_URL, WFS_PARAMS)
            results = json.loads(r.text)

    return render(request, template_name, {'results': results})


def autocomplete_search(request):
    layer_id = request.GET.get('layer', 'purm_stembureaus_2018')

    cql_filter = "({} ILIKE '%{}%')"
    filter_list = []
    layer = Layer.objects.get(layer_id=layer_id)
    search_fields = layer._search_fields #pylint: disable=protected-access
    WFS_PARAMS['typeName'] = layer.layer_name

    if request.is_ajax():
        results = []

        query = request.GET.get('term', '')

        if query and layer:

            if search_fields:
                for field in search_fields.split():
                    filter_list.append(cql_filter.format(field, query))

                cql_filter = ' or '.join(filter_list)
                WFS_PARAMS['CQL_FILTER'] = cql_filter

                r = requests.get(settings.WFS_URL, WFS_PARAMS)
                results = json.loads(r.text)['features']
                results = [x['properties'] for x in results]
                results = [x[field] for x in results] #pylint: disable=undefined-loop-variable
                results = json.dumps(results)
    mimetype = 'application/json'

    return HttpResponse(results, mimetype)

@xframe_options_exempt
def embed(request):
    authorized_layers = Layer.authorized.user_or_group(request.user, is_ctrix(request))
    visible_layers = authorized_layers.filter(~Q(not_in_atlas=True))

    context = {
        'data': {
            'is_embed': True,
            'config': _get_config(request),
            'user': _get_user(request),
            'layers': _default_layers() + [ layer.to_dict() for layer in visible_layers ]
        }
    }

    return render(request, 'v3/app.html', context)

def v3(request, theme_slug=''):
    authorized_layers = Layer.authorized.user_or_group(request.user, is_ctrix(request))
    themes = Theme.objects.all()

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
        'layers': _default_layers() + [ layer.to_dict() for layer in visible_layers ],
        'themes': [ theme.to_dict() for theme in themes ]
    }

    return render(request, 'v3/app.html', context)

def v3_help(request):
    return render(request, 'v3/help.html', {
        'title': 'Help',
        'content': help_content
    })

def v3_disclaimer(request):
    if config.DISCLAIMER:
        return render(request, 'v3/disclaimer.html', {
            'title': 'Disclaimer',
            'content': config.DISCLAIMER,
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

def v3_token(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'token': request.session.get('oidc_access_token')
        })

    return HttpResponse('Unauthorized', status=401)

@login_required(login_url='admin:login')
def v3_admin(request):
    if not request.user.is_superuser:
        return redirect(reverse('admin:login'))

    authorized_layers = Layer.authorized.user_or_group(request.user, is_ctrix(request))
    visible_layers = authorized_layers.filter(~Q(not_in_atlas=True))

    context = {
        'data':  {
            'config': _get_config(request),
            'user': _get_user(request),
            'layers': _default_layers() + [ layer.to_dict() for layer in visible_layers ]
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

def _get_config(request):
    return {
        'organization_name': config.ORGANIZATION_NAME,
        'position': {
            'zoom': config.POSITION_ZOOM,
            'center': {
                'x': config.POSITION_CENTER_X,
                'y': config.POSITION_CENTER_Y
            }
        },
        'suggest_municipalities': config.SUGGEST_MUNICIPALITIES,
        'feature_show_themes': config.FEATURE_SHOW_THEMES,
        'show_disclaimer': config.DISCLAIMER != '',
        'viewers': [ viewer.to_dict() for viewer in Viewer.visible.for_request(request) ],
    }

def _get_user(request):
    user = request.user

    if not user.is_authenticated:
        return None

    return {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name
    }
