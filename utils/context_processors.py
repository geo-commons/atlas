import logging
from django.conf import settings
from webservice.models import Viewer

logger = logging.getLogger(__name__)


def global_settings(request):
    street_smart = Viewer.visible.for_request(
        request).filter(type=Viewer.TYPE_STREET_SMART)
    google_maps = Viewer.visible.for_request(
        request).filter(type=Viewer.TYPE_GOOGLE_MAPS)

    return {
        'street_smart': street_smart[0] if len(street_smart) > 0 else None,
        'google_maps': google_maps[0] if len(google_maps) > 0 else None,
        'SMARTSTREET_USER': settings.SMARTSTREET_USER,
        'SMARTSTREET_PASSWORD': settings.SMARTSTREET_PASSWORD,
        'SMARTSTREET_API_KEY': settings.SMARTSTREET_API_KEY,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'SENTRY_DSN': settings.SENTRY_DSN,
        'AUTHENTICATION_ENABLE_CREDENTIALS': settings.AUTHENTICATION_ENABLE_CREDENTIALS,
        'AUTHENTICATION_ENABLE_OIDC': settings.AUTHENTICATION_ENABLE_OIDC
    }


def homepage(request):
    return {
        'homepage': True
    }
