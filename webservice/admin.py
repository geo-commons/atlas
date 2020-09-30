from django.contrib import admin

from .forms import LayerForm
from .models import Category, Layer, AtlasTheme


class LayerAdmin(admin.ModelAdmin):
    form = LayerForm

    list_display = ('ordering', 'title', 'layer_type', 'closed_dataset',
                    'published')
    list_display_links = ('title',)
    list_editable = ('ordering',)
    list_filter = ('layer_type', 'closed_dataset')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('ordering', 'title')
    list_display_links = ('title',)
    list_editable = ('ordering',)


admin.site.register(Layer, LayerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(AtlasTheme, admin.ModelAdmin)
