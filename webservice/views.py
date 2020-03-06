from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from utils.context_processors import is_ctrix

from .models import AtlasTheme, Category, Layer


class CategoryDetailView(TemplateView):
    template_name = "main_content.html"

    def get_context_data(self, **kwargs):
        slug = kwargs['slug']
        user = self.request.user
        ctrix = is_ctrix(self.request)

        context = super().get_context_data(**kwargs)
        themes = Category.environment_dependent.environment(
            ctrix).filter(slug=slug)

        result = {}

        for theme in themes:
            result[theme] = Layer.authorized.user_or_group(
                user, ctrix).filter(layer_type=theme)
        context['themes'] = result

        return context


class LayerDetailView(TemplateView):
    template_name = "main_content.html"

    def get_context_data(self, **kwargs):
        # slug = kwargs['slug']
        layer_id = kwargs['layer_id']
        user = self.request.user
        ctrix = is_ctrix(self.request)

        context = super().get_context_data(**kwargs)
        # theme = Category.environment_dependent.environment(
        #     ctrix).get(slug=slug)

        result = {}
        layer = Layer.authorized.user_or_group(
            user, ctrix).get(layer_id=layer_id)
        layer.visible = True
        category = layer.layer_type
        result[category] = [layer]
        context['themes'] = result

        return context


class AtlasThemeDetailView(DetailView):
    template_name = "main_content.html"

    model = AtlasTheme

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        ctrix = is_ctrix(self.request)
        context['themes'] = {}
        layers = Layer.authorized.user_or_group(
            user, ctrix).filter(atlastheme=context['atlastheme'])
        context['themes'][context['atlastheme']] = layers
        context['homepage'] = False

        return context


class CategoryListView(ListView):
    "Not used in real life."
    template_name = "main_content.html"
    model = Category
