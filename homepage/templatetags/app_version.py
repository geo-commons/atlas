from django import template
from atlas import VERSION

register = template.Library()

@register.simple_tag
def app_version():
    return VERSION
