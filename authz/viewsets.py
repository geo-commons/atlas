import json
from json import JSONDecodeError
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter

from webservice.mixins import DataExportImportMixin, DuplicateMixin
from webservice.models import Source
from .lib import can_access_source, authorize_ows_request, authorize_wmts_request, authorize_rest_request
from .models import Authorization
from .serializers import AuthorizationSerializer


class AuthorizeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request):
        try:
            data = json.loads(request.body)
        except JSONDecodeError:
            return JsonResponse({
                'result': False,
                'status': 400,
                'message': 'unable to decode json request body'
            }, status=400)

        source_slug = data.get('source')
        if not source_slug:
            return JsonResponse({
                'result': False,
                'status': 400,
                'message': 'source is not defined'
            }, status=400)

        try:
            source = Source.objects.get(slug=source_slug)
        except Source.DoesNotExist:
            return JsonResponse({
                'result': False,
                'status': 400,
                'message': f'could not find source with slug {source_slug}'
            }, status=400)

        if not can_access_source(request, source):
            return JsonResponse({
                'result': False,
                'status': 403 if request.user.is_authenticated else 401,
                'message': f'user {request.user} does not have access to source {source_slug}'
            }, status=403 if request.user.is_authenticated else 401)

        if source.source_type == Source.SOURCE_OWS:
            return authorize_ows_request(source, request, data)
        if source.source_type == Source.SOURCE_WMTS:
            return authorize_wmts_request(source, request, data)
        if source.source_type == Source.SOURCE_REST:
            return authorize_rest_request(source, request, data)

        return JsonResponse({
            'result': False,
            'status': 500,
            'message': 'there is no authorizer for this source type provided'
        }, status=500)


class AuthorizationViewSet(DataExportImportMixin, DuplicateMixin, viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'patch']
    permission_classes = [permissions.IsAdminUser]
    queryset = Authorization.objects.all()
    serializer_class = AuthorizationSerializer

    search_fields = ['resource']

    filter_backends = [SearchFilter, DjangoFilterBackend]
