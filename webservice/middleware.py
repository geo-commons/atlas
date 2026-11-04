from uuid import uuid4


class MapAuditEventRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/atlas/api/v1/maps/"):
            request.audit_event_request_id = uuid4()
        return self.get_response(request)
