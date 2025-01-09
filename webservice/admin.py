from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from import_export.formats import base_formats
from reversion.admin import VersionAdmin

from .forms import LayerForm, LinkedDataForm
from .models import Source, Category, Layer, Template, Selection, Map, MapLayer, LinkedData, Viewer, Dataset, Theme
from .resources import CategoryResource, LayerResource, SourceResource, SelectionResource, MapResource, ThemeResource, \
    DatasetResource


class LinkedDataInline(admin.TabularInline):
    form = LinkedDataForm
    model = LinkedData
    extra = 0


class TemplateInline(admin.StackedInline):
    model = Template
    extra = 0


class MapLayerInline(admin.TabularInline):
    model = MapLayer
    extra = 0


@admin.action(description='Geselecteerde kaartlagen dupliceren')
def duplicate_layer(_modeladmin, _request, queryset):
    for layer in queryset.all():
        layer.pk = None
        layer.published = False

        i = 2
        while Layer.objects.filter(title=f'{layer.title} ({i})').count() > 0:
            i += 1

        layer.title = f'{layer.title} ({i})'
        layer.save()


class CustomImportExportActionModelAdmin(ImportExportActionModelAdmin):
    def get_export_formats(self):
        formats = (
            base_formats.JSON,
            base_formats.CSV,
        )

        return [f for f in formats if f().can_export()]

    def get_import_formats(self):
        formats = (
            base_formats.JSON,
            base_formats.CSV,
        )

        return [f for f in formats if f().can_import()]

    class Meta:
        abstract = True


class SourceAdmin(VersionAdmin, CustomImportExportActionModelAdmin):
    list_display = ('title',)
    resource_classes = [SourceResource]
    filter_horizontal = ('atlas_groups',)
    prepopulated_fields = {'slug': ('title',)}


class LayerAdmin(VersionAdmin, CustomImportExportActionModelAdmin):
    form = LayerForm

    list_display = ('ordering', 'title', 'layer_type', 'closed_dataset', 'login_required',
                    'published')
    list_display_links = ('title',)
    list_editable = ('ordering',)
    list_filter = ('layer_type', 'closed_dataset', 'login_required')

    filter_horizontal = ('atlas_groups',)
    prepopulated_fields = {'slug': ('title',)}

    actions = [duplicate_layer]

    resource_classes = [LayerResource]

    inlines = [
        LinkedDataInline,
        TemplateInline,
    ]

    save_as = True

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'layer_type', 'published')
        }),
        ('Bron', {
            'fields': ('layer_source', 'layer_name', 'source_type', 'projection', 'server_type', 'format')
        }),
        ('Weergave', {
            'fields': (
                'opacity',
                'is_base',
                'is_visible',
                'is_selectable',
                'use_html_info_format',
                'show_in_detail_panel',
                'not_in_atlas',
                '_popup_attributes',
                '_search_fields',
                'extent_min_x',
                'extent_min_y',
                'extent_max_x',
                'extent_max_y',
                'zoom_min',
                'zoom_max',
                'server_style',
                'client_style',
                'friendly_fields',
                'templated_properties',
                'legend_url'
            )
        }),
        ('Metadata', {
            'fields': (
                'meta_name',
                'meta_description',
                'meta_lineage',
                'meta_org',
                'meta_contact',
                'meta_updated',
                'meta_link',
                'dataset'
            )
        }),
        ('Toegang', {
            'fields': ('closed_dataset', 'login_required', 'atlas_groups')
        })
    )

    search_fields = ['title']


class CategoryAdmin(VersionAdmin, CustomImportExportActionModelAdmin):
    list_display = ('ordering', 'title')
    list_display_links = ('title',)
    list_editable = ('ordering',)
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    resource_classes = [CategoryResource]


class SelectionAdmin(VersionAdmin, CustomImportExportActionModelAdmin):
    list_display = ('title',)
    fields = ('title', 'slug', 'layers', 'login_required')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('layers',)

    search_fields = ['title']
    resource_classes = [SelectionResource]


class MapAdmin(VersionAdmin, CustomImportExportActionModelAdmin):
    list_display = ('title',)
    fields = ('title', 'slug', 'features', 'settings', 'description', 'thumbnail', 'published', 'show_in_overview')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ()

    search_fields = ['title']
    resource_classes = [MapResource]

    inlines = [
        MapLayerInline,
    ]


class ViewerAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('ordering', 'label', 'type',)
    list_display_links = ('label',)
    list_editable = ('ordering',)


class DatasetAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('title',)
    list_display_links = ('title',)

    resource_classes = [DatasetResource]
    prepopulated_fields = {'slug': ('title',)}


class ThemeAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('title',)
    list_display_links = ('title',)

    resource_classes = [ThemeResource]
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Source, SourceAdmin)
admin.site.register(Layer, LayerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Selection, SelectionAdmin)
admin.site.register(Map, MapAdmin)
admin.site.register(Viewer, ViewerAdmin)
admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Theme, ThemeAdmin)
