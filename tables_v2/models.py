from django.db import models
from django_extensions.db.fields import AutoSlugField

from webservice.models import Source


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

    # ows tables
    list_cql_filters = models.JSONField(null=True,
                                        blank=True)  # { straatnaam: "{{straatnaam}}", adres: "{{straatnaam}} {{huisnummer}}" }
    detail_cql_filters = models.JSONField(null=True,
                                          blank=True)  # { straatnaam: "{{straatnaam}}", adres: "{{straatnaam}} {{huisnummer}}", staatId: "{{id}}"  }

    tables = models.ManyToManyField(
        'self',
        through='TableToTable',
        symmetrical=False,
        related_name='related_tables'
    )

    class Meta:
        verbose_name = 'Tabel'
        verbose_name_plural = 'Tabellen'
        ordering = ['title']

    def __str__(self):
        return f"{self.title}"


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

