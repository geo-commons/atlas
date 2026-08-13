from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from import_export.formats import base_formats
from reversion.admin import VersionAdmin

from .forms import LayerForm, LinkedDataForm
from .models import Source, Category, Layer, Template, Map, MapLayer, LinkedData, Viewer
from .resources import CategoryResource, LayerResource, SourceResource, MapResource


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

    list_display = ('ordering', 'title', 'layer_type', 'closed_dataset', 'login_required')
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
            'fields': ('title', 'slug', 'layer_type', 'is_exportable')
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
                'is_filterable_in_legend',
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
                'legend_url',
                '_search_terms',
            )
        }),
        ('Metadata', {
            'fields': (
                'metadataset',
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


admin.site.register(Source, SourceAdmin)
admin.site.register(Layer, LayerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Map, MapAdmin)
admin.site.register(Viewer, ViewerAdmin)
