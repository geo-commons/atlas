from django.core.exceptions import SuspiciousOperation

from utils.tools import is_internal
from .models import Layer


def authorize_ows_request(request, source):
    query_params = get_query_parameters_as_lowercase(request)
    service = query_params.get('service')

    visible_layers_for_source = Layer.authorized.for_request(
        request).prefetch_related('atlas_groups').filter(layer_source=source)

    accessible_layers = []
    for layer in visible_layers_for_source:
        if can_request_access_layer(request, layer):
            accessible_layers.append(layer.layer_name)

    if service == 'WMS':
        wms_request = query_params.get('request')
        if wms_request in ['GetMap', 'GetFeatureInfo', 'DescribeLayer']:
            requested_layers = query_params.get('layers').split(',')
            return set(requested_layers).issubset(accessible_layers)
        if wms_request == 'GetLegendGraphic':
            requested_layer = query_params.get('layer')
            return requested_layer in accessible_layers
        if wms_request == 'GetCapabilities':
            return request.user.is_authenticated
    if service == 'WFS':
        wfs_request = query_params.get('request')
        if wfs_request in ['DescribeFeatureType', 'GetFeature']:
            if query_params.get('typename'):
                requested_layers = query_params.get('typename').split(',')

            if query_params.get('typenames'):
                requested_layers += query_params.get('typenames').split(',')

            return set(requested_layers).issubset(accessible_layers)
        if wfs_request == 'GetCapabilities':
            return request.user.is_authenticated

    return False


def authorize_wmts_request(request, source):
    query_params = request.GET.lower()
    service = query_params.get('service')

    visible_layers_for_source = Layer.authorized.for_request(
        request).prefetch_related('atlas_groups').filter(layer_source=source)

    accessible_layers = []
    for layer in visible_layers_for_source:
        if can_request_access_layer(request, layer):
            accessible_layers.append(layer.layer_name)

    if service == 'WMTS':
        wmts_request = query_params.get('request')
        if wmts_request == 'GetTile':
            requested_layer = query_params.get('layer')
            return requested_layer in accessible_layers

    return False


def can_request_access_layer(request, layer):
    user = request.user

    if not layer.is_published:
        return False

    if layer.closed_dataset and is_internal(request) is not True:
        return False

    if layer.login_required and user.is_anonymous:
        return False

    layer_only_accessible_by_groups = layer.atlas_groups.exists()

    if user.is_anonymous and not layer_only_accessible_by_groups:
        return True

    if user.is_anonymous and layer_only_accessible_by_groups:
        return False

    if not user.is_anonymous and not layer_only_accessible_by_groups:
        return True

    user_groups = user.atlas_groups.all()
    user_has_access_to_layer_via_group = any(
        g for g in layer.atlas_groups.all() if g in user_groups
    )

    if not user.is_anonymous and user_has_access_to_layer_via_group:
        return True

    if not user.is_anonymous and not user_has_access_to_layer_via_group:
        return False

    return False


def can_request_access_source(request, source):
    user = request.user

    if source.login_required and user.is_anonymous:
        return False

    source_only_accessible_by_groups = source.atlas_groups.exists()

    if user.is_anonymous and not source_only_accessible_by_groups:
        return True

    if user.is_anonymous and source_only_accessible_by_groups:
        return False

    if not user.is_anonymous and not source_only_accessible_by_groups:
        return True

    user_groups = user.atlas_groups.all()
    user_has_access_to_source_via_group = any(
        g for g in source.atlas_groups.all() if g in user_groups
    )

    if not user.is_anonymous and user_has_access_to_source_via_group:
        return True

    if not user.is_anonymous and not user_has_access_to_source_via_group:
        return False

    return False


def get_query_parameters_as_lowercase(request):
    query_parameters = {}

    for key, value in request.GET.items():
        folded_key = key.casefold()

        if folded_key in query_parameters:
            raise SuspiciousOperation(
                'You are trying to set multiple query parameter keys')

        query_parameters[folded_key] = value

    return query_parameters
