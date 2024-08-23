import ipaddress
import logging
from django.conf import settings
from django.utils.text import slugify

logger = logging.getLogger(__name__)


def is_internal(request):
    if not settings.INTERNAL_IPS:
        return False

    client_ip = get_client_ip(request)

    if not client_ip:
        return False

    return ip_in_one_of_ranges(client_ip, settings.INTERNAL_IPS)


def is_allowed_to_access_admin(request):
    if not settings.ADMIN_IPS:
        return True

    client_ip = get_client_ip(request)

    if not client_ip:
        return False

    return ip_in_one_of_ranges(client_ip, settings.ADMIN_IPS)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    try:
        return ipaddress.ip_address(ip)
    except ValueError:
        return None


def ip_in_one_of_ranges(ip, ip_ranges):
    for ip_range in ip_ranges:
        if ip in ipaddress.ip_network(ip_range):
            return True

    return False


def generate_unique_slug(model, slug_base):
    slug_base = slugify(slug_base)
    generated_slug = slug_base

    queryset = model.__class__.objects.filter(slug=generated_slug)
    count = 1
    while queryset.exists():
        generated_slug = f'{slug_base}{count}'
        queryset = model.__class__.objects.filter(slug=generated_slug)
        count += 1

    return generated_slug
