from constance.admin import get_values

from utils.decorators import request_cache


@request_cache
def get_constance_config(request):
    return get_values()
