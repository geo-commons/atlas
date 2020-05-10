import logging

from django.conf import settings
from django.http import HttpRequest

logger = logging.getLogger(__name__)

def global_settings(request):
    return {
        'SMARTSTREET_USER': settings.SMARTSTREET_USER,
        'SMARTSTREET_PASSWORD': settings.SMARTSTREET_PASSWORD,
        'SMARTSTREET_API_KEY': settings.SMARTSTREET_API_KEY,
        'WFS_URL_CTRIX': settings.WFS_URL_CTRIX,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'SENTRY_DSN': settings.SENTRY_DSN,
        'MATOMO_URL': settings.MATOMO_URL,
        'MATOMO_SITE_ID': settings.MATOMO_SITE_ID
    }

def is_ctrix(request: HttpRequest) -> bool:
    """Check if ip address of the visitor is listed as a ctrix ip address. """

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    logger.info("IP: %s", ip)

    return ip in settings.CTRIX_IPS


def ctrix_context(request):
    return {
        'ctrix': is_ctrix(request)
    }


def homepage(request):
    return {
        'homepage': True
    }
