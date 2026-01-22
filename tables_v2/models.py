from django.db import models
from django_extensions.db.fields import AutoSlugField

from webservice.models import Source


# TODO: Rename model name TableTemp to a better name (maybe just table?)
class TableTemp(models.Model):
    title = models.CharField('Naam', max_length=128,
                             help_text="De naam van de tabel")
    slug = AutoSlugField('Kort kenmerk', null=True, default=None, blank=False, unique=True, populate_from='title',
                         overwrite_on_add=False, editable=True,
                         help_text='Een uniek kort kenmerk voor de tabel in Atlas. Gebruik alleen kleine letters, cijfers en afbreekstreepjes.',
                         max_length=255)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    source_type = models.CharField('Brontype', choices=Source.SOURCE_TYPES, default=Source.SOURCE_OWS)
    fields = models.JSONField(null=True, blank=True)

    # rest tables
    list_endpoint = models.CharField('List endpoint', max_length=1024, null=True,
                                     blank=True, )  # /zoeken/&straatnaam={{straatNaam}}&postCode={{postCode}}+{{variable}}
    detail_endpoint = models.CharField('Detail endpoint', max_length=1024, null=True,
                                       blank=True, )  # /zoeken/?id={{id}}
    list_property = models.CharField('Veldnaam van lijst',
                                  max_length=255, blank=True, null=True)
    detail_property = models.CharField('Veldnaam van detailweergave',
                                       max_length=255, blank=True, null=True)
    page_param = models.CharField('URL parameter voor pagina',
                                      max_length=255, blank=True, null=True)
    items_per_page_param = models.CharField('URL parameter voor items per pagina',
                                                max_length=255, blank=True, null=True)
    total_items_page_property = models.CharField('Veldnaam van totaal aantal items',
                                                  max_length=255, blank=True, null=True)
    list_error_property = models.CharField('Veldnaam van foutmelding in lijstweergave', max_length=255, blank=True, null=True)
    detail_error_property = models.CharField('Veldnaam van foutmelding detailweergave', max_length=255, blank=True, null=True)
    template_fields = models.JSONField('Templatevelden', default=dict, blank=True, null=True)

    # ows tables
    layer_name = models.CharField(
        'Laagnaam', max_length=128, null=True, help_text='De naam van de laag op de geoserver.')
    list_cql_filters = models.JSONField(null=True,
                                        blank=True)  # { straatnaam: "{{straatnaam}}", adres: "{{straatnaam}} {{huisnummer}}" }
    detail_cql_filters = models.JSONField(null=True,
                                          blank=True)  # { straatnaam: "{{straatnaam}}", adres: "{{straatnaam}} {{huisnummer}}", staatId: "{{id}}"  }

    # Display properties for columns
    list_display_properties = models.JSONField('Kolommen voor lijstweergave', null=True, blank=True, default=list,
                                               help_text='Lijst van kolomnamen die getoond worden in de lijstweergave')
    detail_display_properties = models.JSONField('Kolommen voor detailweergave', null=True, blank=True, default=list,
                                                 help_text='Lijst van kolomnamen die getoond worden in de detailweergave')

    tables = models.ManyToManyField(
        'self',
        through='TableToTable',
        symmetrical=False,
        related_name='related_tables'
    )

    layers = models.ManyToManyField(
        'webservice.Layer',
        through='LayerToTable',
        related_name='related_tables'
    )

    class Meta:
        verbose_name = 'Tabel'
        verbose_name_plural = 'Tabellen'
        ordering = ['title']

    def __str__(self):
        return f"{self.title}"

    def to_dict(self, from_layer=None):
        data = {
            'id': self.pk,
            'title': self.title,
            'slug': self.slug,
            'source': self.source.to_dict(),
            'source_type': self.source_type,
            'fields': self.fields,
            'list_endpoint': self.list_endpoint,
            'detail_endpoint': self.detail_endpoint,
            'list_property': self.list_property,
            'detail_property': self.detail_property,
            'page_param': self.page_param,
            'items_per_page_param': self.items_per_page_param,
            'total_items_page_property': self.total_items_page_property,
            'list_error_property': self.list_error_property,
            'detail_error_property': self.detail_error_property,
            'layer_name': self.layer_name,
            'list_cql_filters': self.list_cql_filters,
            'detail_cql_filters': self.detail_cql_filters,
            'list_display_properties': self.list_display_properties,
            'detail_display_properties': self.detail_display_properties,
            'template_fields': self.template_fields,
            'related_tables': [item.simple_to_dict(self) for item in self.tables.all()],
        }

        if from_layer:
            try:
                layer_to_table = LayerToTable.objects.get(from_layer=from_layer, to_table=self)
                data['field_mapping'] = layer_to_table.field_mapping
            except LayerToTable.DoesNotExist:
                data['field_mapping'] = None

        return data

    # A simpler version without related tables to prevent loops
    def simple_to_dict(self, from_table=None):
        data = {'to_table': {
            'id': self.pk,
            'title': self.title,
            'slug': self.slug,
            'source': self.source.to_dict(),
            'source_type': self.source_type,
            'fields': self.fields,
            'list_endpoint': self.list_endpoint,
            'detail_endpoint': self.detail_endpoint,
            'list_property': self.list_property,
            'detail_property': self.detail_property,
            'page_param': self.page_param,
            'items_per_page_param': self.items_per_page_param,
            'total_items_page_property': self.total_items_page_property,
            'list_error_property': self.list_error_property,
            'detail_error_property': self.detail_error_property,
            'layer_name': self.layer_name,
            'list_cql_filters': self.list_cql_filters,
            'detail_cql_filters': self.detail_cql_filters,
            'list_display_properties': self.list_display_properties,
            'detail_display_properties': self.detail_display_properties,
            'template_fields': self.template_fields,
        }}

        if from_table:
            try:
                table_to_table = TableToTable.objects.get(from_table=from_table, to_table=self)
                data['field_mapping'] = table_to_table.field_mapping
            except TableToTable.DoesNotExist:
                data['field_mapping'] = None

        return data


class TableToTable(models.Model):
    from_table = models.ForeignKey('TableTemp', related_name='outgoing_table_relations', on_delete=models.CASCADE)
    to_table = models.ForeignKey('TableTemp', related_name='incoming_table_relations', on_delete=models.CASCADE)
    field_mapping = models.JSONField('Mapping van kolomnamen')
    '''
    from = adres
    to = ligplaats

    mapping = {
        ligplaatsnummer: ligplaatsnummer2,

    }
    '''

    class Meta:
        unique_together = ('from_table', 'to_table')


class LayerToTable(models.Model):
    from_layer = models.ForeignKey('webservice.Layer', related_name='layer_table_relations', on_delete=models.CASCADE)
    to_table = models.ForeignKey('TableTemp', related_name='layer_table_relations', on_delete=models.CASCADE)
    field_mapping = models.JSONField('Mapping van kolomnamen')
    '''
        from = adres
        to = ligplaats

        mapping = {
            ligplaatsnummer: ligplaatsnummer2,

        }
        '''

    class Meta:
        unique_together = ('from_layer', 'to_table')
