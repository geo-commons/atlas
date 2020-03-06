import logging

from django.core.exceptions import PermissionDenied
from django.urls import reverse

from .context_processors import is_ctrix


logger = logging.getLogger(__name__)


def check_access_admin(get_response):
    """Middleware to intercept request to deny access to forbidden pages."""

    admin_url = reverse('admin:login').replace('login/', '')
    formidden_urls = [reverse('homepage:downloads')]

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        path = request.path
        logger.info("Path: %s is_ctrix: %s", path, is_ctrix(request))

        if not request.user.is_anonymous and not is_ctrix(request):
            logger.warning("Flush user session.")
            request.session.flush()

        if (path.startswith(admin_url)
                or path in formidden_urls) and not is_ctrix(request):
            request.session.flush()
            logger.warning("Trying to access page within CTRIX.")
            raise PermissionDenied

        response = get_response(request)

        return response

    return middleware
