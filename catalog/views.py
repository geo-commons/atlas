from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Dataset
from .filters import DatasetFilter


def index(request):
    return render(request, 'index.html')


class DatasetListView(ListView):
    model = Dataset
    paginate_by = 10
    text_search_label = ""
    text_search_fields = ["title"]

    def get_queryset(self):
        self.case_filter = DatasetFilter(
            self.request.GET, queryset=super().get_queryset(), request=self.request)
        return self.case_filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.case_filter.form
        return context


class DatasetDetailView(DetailView):
    model = Dataset
