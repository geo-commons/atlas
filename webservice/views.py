from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from utils.tools import is_internal

from .models import Map, Category, Layer


class CategoryDetailView(TemplateView):
    template_name = "main_content.html"

    def get_context_data(self, **kwargs):
        user = self.request.user

        context = super().get_context_data(**kwargs)
        context['layers'] = Layer.authorized.user_or_group(
            user, is_internal(self.request))

        return context


class LayerDetailView(TemplateView):
    template_name = "main_content.html"

    def get_context_data(self, **kwargs):
        user = self.request.user

        layer = Layer.authorized.user_or_group(
            user, is_internal(self.request)).get(slug=kwargs['slug'])

        context = super().get_context_data(**kwargs)
        context['layers'] = [layer]

        return context


class MapDetailView(DetailView):
    template_name = "main_content.html"

    model = Map

    def get_context_data(self, **kwargs):
        user = self.request.user

        context = super().get_context_data(**kwargs)
        context['layers'] = Layer.authorized.user_or_group(
            user, is_internal(self.request)).filter(atlastheme=context['atlastheme'])
        context['homepage'] = False

        return context


class CategoryListView(ListView):
    "Not used in real life."
    template_name = "main_content.html"
    model = Category
