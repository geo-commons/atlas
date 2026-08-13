from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse

from utils.tools import is_internal
from webservice.models import Layer
from .models import Authorization, Log


def authorize_ows_request(source, request, data):
    user = request.user

    resource = data.get('resource')
    if not resource:
        return JsonResponse({'result': False, 'status': 400, 'message': 'resource is not specified'}, status=400)

    authorization_rules = Authorization.objects.filter(
        source=source,
        resource=data.get('resource')
    ).prefetch_related('atlas_groups')

    if len(authorization_rules) > 0:
        for authorization in authorization_rules:
            is_transaction = data.get('request') == 'Transaction'

            authorized = ((is_transaction and authorization.is_mutable_by(user, request) and authorization.is_accessible_by(user, request)) or
                          (not is_transaction and authorization.is_accessible_by(user, request)))

            if authorized:
                should_log = authorization.audit_log and (
                    is_transaction or data.get('request') in ['GetFeatureInfo', 'GetFeature'])

                if should_log:
                    Log.objects.create(
                        username=user.username if user.is_authenticated else 'anonymous',
                        email=user.email if user.is_authenticated else '',
                        user_agent=data.get('user_agent'),
                        ip=data.get('ip'),
                        source=source.slug,
                        resource=data.get('resource'),
                        params=data.get('params')
                    )

                data = {
                    'result': True,
                    'status': 200,
                    'username': user.username if user.is_authenticated else 'anonymous'
                }

                if authorization.response_filter:
                    data['response_filter'] = authorization.response_filter

                return JsonResponse(data)

        return JsonResponse({
            'result': False,
            'status': 403 if user.is_authenticated else 401,
            'message': f'user {user} does not have access to layer {resource}'
        }, status=403 if user.is_authenticated else 401)

    layer_rules = Layer.objects.filter(
        layer_source=source,
        layer_name=data.get('resource')
    ).prefetch_related('atlas_groups')

    for layer in layer_rules:
        if layer.is_accessible_by(user, request) and data.get('request') not in ['Transaction']:
            return JsonResponse({'result': True, 'status': 200, 'username': user.username if user.is_authenticated else 'anonymous'})

    write_layer_rules = Layer.objects.filter(
        layer_source=source,
        layer_name=data.get('resource')
    ).prefetch_related('atlas_write_groups')

    for layer in write_layer_rules:
        if layer.is_mutable_by(user, request) and layer.is_accessible_by(user, request) and data.get('request') in ['Transaction']:
            return JsonResponse({'result': True, 'status': 200, 'username': user.username if user.is_authenticated else 'anonymous'})

    return JsonResponse({
        'result': False,
        'status': 403 if user.is_authenticated else 401,
        'message': f'user {user} does not have access to layer {resource}'
    }, status=403 if user.is_authenticated else 401)


def authorize_wmts_request(source, request, data):
    user = request.user

    resource = data.get('resource')
    if not resource:
        return JsonResponse({'result': False, 'status': 400, 'message': 'resource is not specified'}, status=400)

    authorization_rules = Authorization.objects.filter(
        source=source,
        resource=data.get('resource')
    ).prefetch_related('atlas_groups')

    if len(authorization_rules) > 0:
        for authorization in authorization_rules:
            if authorization.is_accessible_by(user, request):
                data = {
                    'result': True,
                    'status': 200,
                    'username': user.username if user.is_authenticated else 'anonymous'
                }
                return JsonResponse(data)

        return JsonResponse({
            'result': False,
            'status': 403 if user.is_authenticated else 401,
            'message': f'user {user} does not have access to layer {resource}'
        }, status=403 if user.is_authenticated else 401)

    layer_rules = Layer.objects.filter(
        layer_source=source,
        layer_name=data.get('resource')
    ).prefetch_related('atlas_groups')

    for layer in layer_rules:
        if layer.is_accessible_by(user, request):
            return JsonResponse({'result': True, 'status': 200, 'username': user.username if user.is_authenticated else 'anonymous'})

    return JsonResponse({
        'result': False,
        'status': 403 if user.is_authenticated else 401,
        'message': f'user {user} does not have access to layer {resource}'
    }, status=403 if user.is_authenticated else 401)


def authorize_rest_request(source, request, data):
    user = request.user

    resource = data.get('resource')
    if not resource:
        return JsonResponse({'result': False, 'status': 400, 'message': 'resource is not specified'}, status=400)

    authorization_rules = Authorization.objects.filter(
        source=source,
        resource=data.get('resource')
    ).prefetch_related('atlas_groups')

    if len(authorization_rules) > 0:
        for authorization in authorization_rules:
            if authorization.is_accessible_by(user, request):
                if authorization.audit_log:
                    Log.objects.create(
                        username=user.username if user.is_authenticated else 'anonymous',
                        email=user.email if user.is_authenticated else '',
                        user_agent=data.get('user_agent'),
                        ip=data.get('ip'),
                        source=source.slug,
                        resource=data.get('resource'),
                        params=data.get('params')
                    )
                data = {
                    'result': True,
                    'status': 200,
                    'username': user.username if user.is_authenticated else 'anonymous'
                }

                if authorization.response_filter:
                    data['response_filter'] = authorization.response_filter
                return JsonResponse(data)

    return JsonResponse({
        'result': False,
        'status': 403 if user.is_authenticated else 401,
        'message': f'user {user} does not have access to resource {resource}'
    }, status=403 if user.is_authenticated else 401)


def can_access_source(request, source):
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

# TODO: We should check if we can combine this function with the is_accesible_by method on a Layer model. Issue: https://gitlab.com/purmerend/atlas/-/issues/805


def can_request_access_layer(request, layer):
    user = request.user

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


def get_query_parameters_as_lowercase(request):
    query_parameters = {}

    for key, value in request.GET.items():
        folded_key = key.casefold()

        if folded_key in query_parameters:
            raise SuspiciousOperation(
                'You are trying to set multiple query parameter keys')

        query_parameters[folded_key] = value

    return query_parameters
