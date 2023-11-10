import base64
import binascii
import json
import logging
import time

from django.contrib.auth import authenticate, logout
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.utils.encoding import smart_bytes
from django.urls import reverse
from josepy.jws import JWS

from .tools import is_allowed_to_access_admin


logger = logging.getLogger(__name__)


def check_access_admin(get_response):
    """Middleware to intercept request to deny access to forbidden pages."""

    forbidden_urls = [
        reverse('admin:index'),
        reverse('homepage:v3_admin')
    ]

    def middleware(request):
        path = request.path

        if is_allowed_to_access_admin(request):
            return get_response(request)

        for forbidden_url in forbidden_urls:
            if path.startswith(forbidden_url):
                return HttpResponseForbidden('Je hebt geen toegang tot deze pagina vanaf deze locatie')

        return get_response(request)

    return middleware


class LogoutWhenOIDCTokenIsExpiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        if not request.session.get('oidc_access_token'):
            return

        token = smart_bytes(request.session.get('oidc_access_token'))
        jws = JWS.from_compact(token)

        try:
            payload = json.loads(jws.payload)
            if payload['exp'] < time.time():
                logout(request)
        except json.JSONDecodeError:
            pass


class BasicAuthForAuthorizationEndpointMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path

        if not path.startswith(reverse('homepage:v3_authorize')):
            return

        if 'HTTP_AUTHORIZATION' not in request.META:
            return

        authorization_header = request.META['HTTP_AUTHORIZATION']
        splitted = authorization_header.split(' ')
        auth_type, auth_string = splitted

        if 'basic' != auth_type.lower():
            return

        try:
            b64_decoded = base64.b64decode(auth_string)
        except (TypeError, binascii.Error):
            return

        try:
            auth_string_decoded = b64_decoded.decode('utf-8')
        except UnicodeDecodeError:
            return

        splitted = auth_string_decoded.split(':')
        if len(splitted) != 2:
            return

        user = authenticate(username=splitted[0], password=splitted[1])

        if user is not None:
            request.user = user
