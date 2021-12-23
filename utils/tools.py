import logging
from django.conf import settings
from django.http import HttpRequest

logger = logging.getLogger(__name__)

def is_ctrix(request: HttpRequest) -> bool:
    """Check if ip address of the visitor is listed as a ctrix ip address. """

    if settings.CTRIX_IPS == ['*']:
        return True

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    logger.info("IP: %s", ip)

    return ip in settings.CTRIX_IPS
