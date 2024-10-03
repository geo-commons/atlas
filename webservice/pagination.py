from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_page_size(self, request):
        if 'page_size' in request.query_params:
            try:
                return int(request.query_params.get(self.page_size_query_param, self.page_size))
            except ValueError:
                return 20
        return super().get_page_size(request)