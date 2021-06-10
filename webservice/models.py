from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django_extensions.db.fields import AutoSlugField

from user_management.models import AtlasGroup


class LayerManager(models.Manager):
    def __closed_unowned_datasets(self):
        return self.filter(closed_dataset=True)\
            .filter(published=True)\
            .filter(users=None)\
            .filter(atlas_groups=None)

    def __closed_dataset_user(self, user):
        return self.filter(users=user).filter(published=True)

    def __closed_dataset_group(self, user):
        return self.filter(published=True).filter(
            atlas_groups__in=user.atlas_groups.all())

    def user_or_group(self, user="", ctrix=False):
        open_dataset = self.filter(closed_dataset=False)\
            .filter(published=True)

        closed_dataset = self.__closed_unowned_datasets()

        if not ctrix:
            return open_dataset

        if user and user.is_anonymous and ctrix:
            result = open_dataset | closed_dataset
            return result

        closed_dataset_user = self.__closed_dataset_user(user)
        closed_dataset_group = self.__closed_dataset_group(user)

        result = open_dataset\
            | closed_dataset\
            | closed_dataset_group\
            | closed_dataset_user

        return result


class Category(models.Model):
    objects = models.Manager()

    title = models.CharField('Titel', max_length=128, null=True)

    slug = AutoSlugField(blank=False, populate_from='title', overwrite=True)
    ordering = models.PositiveIntegerField('Sortering',
                                           default=0, editable=True, db_index=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categorieën'
        ordering = ['ordering', 'title']


class Layer(models.Model):
    SOURCE_WMS_WFS = 'WMS_WFS'
    SOURCE_WMS = 'WMS'
    SOURCE_WMTS = 'WMTS'
    SOURCE_TYPES = [
        (SOURCE_WMS_WFS, 'WMS en WFS'),
        (SOURCE_WMS, 'WMS'),
        (SOURCE_WMTS, 'WMTS')
    ]

    objects = models.Manager()
    authorized = LayerManager()

    layer_id = models.CharField(
        'Laag ID', max_length=128, null=True, default='', help_text='Het unieke kenmerk van de laag in Atlas')
    title = models.CharField('Titel', max_length=128, null=True)
    layer_name = models.CharField(
        'Laagnaam', max_length=128, null=True, help_text='De naam van de laag op de geoserver')

    meta_name = models.CharField('Naam', max_length=128, null=True)
    meta_kind = models.CharField('Soort', max_length=128, null=True)
    meta_org = models.CharField('Organisatie', max_length=128, null=True)
    meta_updated = models.CharField(
        'Laatst bijgewerkt', max_length=128, null=True)

    opacity = models.DecimalField(
        'Ondoorzichtigheid', max_digits=1, decimal_places=1, default=0.9)
    visible = models.BooleanField('Zichtbaar', default=False)

    layer_type = models.ForeignKey(
        Category, verbose_name='Categorie', on_delete=models.SET_NULL,
        blank=True, null=True)

    isqueryable = models.BooleanField('Kan doorzocht worden', default=True,
                                      help_text='Deze instelling is alleen van toepassing op Atlas versie 2 en wordt binnenkort verwijderd')

    _popup_attributes = models.CharField(
        'Toon deze velden', max_length=250, blank=True, null=True)

    _search_fields = models.CharField(
        'Zoek in deze velden', max_length=250, blank=True, null=True)

    projection = models.CharField(
        'Projectie', max_length=100, default='EPSG:28992')

    url = models.CharField(
        'URL',
        max_length=500,
        default='https://datalab.purmerend.nl/geoserver/topp/wms?')

    server_type = models.CharField(
        'Servertype', max_length=50, default='geoserver')

    closed_dataset = models.BooleanField(
        'Besloten', default=True, help_text='Laag is alleen zichtbaar binnen interne omgeving')

    published = models.BooleanField('Gepubliceerd', default=False)

    source_type = models.CharField('Brontype', choices=SOURCE_TYPES, default=SOURCE_WMS_WFS, max_length=20,
                                   help_text='"WMS en WFS" is zichtbaar in zowel het datapaneel als op de kaart. WMS en WMTS toont alleen op de kaart.'
                                   )

    is_base = models.BooleanField('Is basislaag', default=False)
    is_visible = models.BooleanField('Is standaard zichtbaar', default=False)

    not_in_atlas = models.BooleanField(
        'Toon laag alleen in een themakaart',
        default=False,
        help_text='De laag wordt niet getoond in de standaardkaart')

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Eigenaar',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='owner')

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, verbose_name='Gebruikers')
    atlas_groups = models.ManyToManyField(
        AtlasGroup, blank=True, verbose_name='Groepen')

    created_at = models.DateTimeField('created_at', auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True)

    ordering = models.PositiveIntegerField('Sortering',
                                           default=0, editable=True, db_index=True)

    def __str__(self):
        return self.title

    @property
    def popup_attributes(self):
        attributes = self._popup_attributes
        if not attributes:
            return ""
        result = []
        for attr in attributes.split():
            result.append("'{}'".format(attr))
        return "popupAttributes: [{}]".format(", ".join(result))

    @property
    def search_fields(self):
        search_fields = self._search_fields
        if not search_fields:
            return ""
        result = []
        for attr in search_fields.split():
            result.append("'{}'".format(attr))
        return "search_fields: [{}]".format(", ".join(result))

    @property
    def slddiv(self):
        return "sld_div_{}".format(self.layer_id)

    @property
    def layer_type_str(self):
        return 'themelayer:true'

    @property
    def infodiv(self):
        return "info_{}".format(self.layer_id)

    @property
    def sld(self):
        return "sld_{}".format(self.layer_id)

    @property
    def legend(self):
        return "lgn_{}".format(self.layer_id)

    @property
    def filterid(self):
        return "flt_{}".format(self.layer_id)

    @property
    def filterdataid(self):
        return "data_{}".format(self.layer_id)

    @property
    def datazoekid(self):
        return "zoek_data_{}".format(self.layer_id)

    @property
    def params(self):
        return "{{'layers': '{0}'}}".format(self.layer_name)

    @property
    def source(self):
        # TODO: check server_type case.

        return """
source: new ol.source.TileWMS({{
    projection: '{0}',
    url: '{1}',
    params: {2},
    serverType: '{3}'
}})""".format(self.projection, self.url, self.params, self.server_type)

    @property
    def is_published(self):
        return self.published

    @property
    def is_closed_dataset(self):
        return self.closed_dataset

    def to_dict(self):
        return {
            'id': self.layer_id,
            'source_type': self.source_type,
            'title': self.title,
            'name': self.layer_name,
            'opacity': float(self.opacity),
            'url': self.url,
            'server_type': self.server_type,
            'is_base': self.is_base,
            'is_visible': self.is_visible,
            'projection': self.projection,
            'category': {
                'id': self.layer_type.id,
                'title': self.layer_type.title
            } if self.layer_type else None,
            'display_properties': self._popup_attributes.split('\r\n') if self._popup_attributes else [],
            'search_properties': self._search_fields.split('\r\n') if self._search_fields else [],
            'metadata': {
                'description': self.meta_kind,
                'organization': self.meta_org,
                'updated': self.meta_updated
            },
            'linked_data': [item.to_dict() for item in self.linked_data.all()]
        }

    class Meta:
        verbose_name = 'Kaartlaag'
        verbose_name_plural = 'Kaartlagen'
        ordering = ['ordering', 'title']


class LinkedData(models.Model):
    source = models.ForeignKey(
        Layer, on_delete=models.CASCADE, related_name='linked_data')

    title = models.CharField(_('Titel'), max_length=128, null=True)
    layer_name = models.CharField(_('Laag naam'), max_length=128)
    url = models.CharField(_('URL'), max_length=500,
                           default='https://datalab.purmerend.nl/geoserver/topp/wms?')
    source_key = models.CharField(_('Bronsleutel'), max_length=128)
    target_key = models.CharField(_('Doelsleutel'), max_length=128)
    popup_attributes = models.CharField(_('Toon deze velden'), max_length=250, blank=True, null=True,
                                        help_text='Voer één veld per regel in. Bij een leeg veld worden alle velden getoond.')

    class Meta:
        verbose_name = 'Gekoppelde data'
        verbose_name_plural = 'Gekoppelde data'

    def __str__(self):
        return self.layer_name

    def to_dict(self):
        return {
            'title': self.title,
            'name': self.layer_name,
            'url': self.url,
            'source_key': self.source_key,
            'target_key': self.target_key,
            'display_properties': self.popup_attributes.split('\r\n') if self.popup_attributes else []
        }


class AtlasTheme(models.Model):
    title = models.CharField('Titel', max_length=128, null=True)
    slug = AutoSlugField(blank=False, populate_from='title', overwrite=True)
    layers = models.ManyToManyField(Layer)

    def get_absolute_url(self):
        return reverse('webservice:atlastheme-detail',
                       kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Thema'
        verbose_name_plural = "Thema's"

    def __str__(self):
        return f"{self.title}"
