import csv
import json
from datetime import datetime
import logging

import requests
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from utils.context_processors import is_ctrix
from webservice.models import Layer

from .forms import UploadDatasetForm
from .models import SavedDataset


logger = logging.getLogger(__name__)


class HomePageView(TemplateView):
    template_name = "main_content.html"

    def get_context_data(self, **kwargs):
        user = self.request.user

        context = super().get_context_data(**kwargs)
        context['layers'] = Layer.authorized.user_or_group(user, is_ctrix(self.request)).filter(~Q(not_in_atlas=True))

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
            dataset.title = '{}-{}'.format(timestamp,
                                           form.cleaned_data['title'])
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
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.\
            format(dataset.title)

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

    context = {
        'layers': _default_layers() + [ layer.to_dict() for layer in authorized_layers ]
    }

    return render(request, 'embed.html', context)

def v3(request):
    authorized_layers = Layer.authorized.user_or_group(request.user, is_ctrix(request))

    context = {
        'layers': _default_layers() + [ layer.to_dict() for layer in authorized_layers ]
    }

    return render(request, 'v3.html', context)

def _default_layers():
    return [
        {
            'id': 'brt_topo_kaart_totaal',
            'title': 'Kaart grijs',
            'name': 'topp:topografische_kaart_grijs',
            'opacity': 0.9,
            'url': 'https://datalab.purmerend.nl/geoserver/topp/wms',
            'server_type': 'geoserver',
            'is_base': True,
            'is_visible': True
        },
        {
            'id': 'purm_lufo2020',
            'title': 'Luchtfoto 2020',
            'name': 'topp:Lufo_Totaal_2020',
            'opacity': 0.9,
            'url': 'https://datalab.purmerend.nl/geoserver/topp/wms',
            'server_type': 'geoserver',
            'is_base': True,
            'is_visible': False
        },
    ]
