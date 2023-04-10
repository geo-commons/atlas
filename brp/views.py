from django.shortcuts import render
from webservice.models import Layer
from utils.tools import is_ctrix
from django.db.models import Q
from django.shortcuts import render
from homepage.views import _get_config, _get_user, _default_layers

def index(request):
    authorized_layers = Layer.authorized.user_or_group(request.user, is_ctrix(request))

    context = {}

    visible_layers = authorized_layers.filter(~Q(not_in_atlas=True))

    context['data'] = {
        'is_embed': False,
        'config': _get_config(request),
        'user': _get_user(request),
        'layers': _default_layers() + [ layer.to_dict() for layer in visible_layers ]
    }

    return render(request, 'brp/index.html')
