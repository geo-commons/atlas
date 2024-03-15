import json
import logging
import time

from django.contrib.auth import logout
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
