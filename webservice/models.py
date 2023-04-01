from os import path
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.db.models import Q
from django_extensions.db.fields import AutoSlugField

from user_management.models import AtlasGroup
from utils.tools import is_ctrix


class LayerManager(models.Manager):
    def user_or_group(self, user=None, ctrix=False):
        open_datasets = Q(published=True) & Q(closed_dataset=False)
        closed_unassigned_datasets = Q(published=True) & Q(closed_dataset=True) & Q(users=None) & Q(atlas_groups=None)

        if not ctrix:
            return self.filter(open_datasets).distinct()

        if user.is_anonymous:
            return self.filter(open_datasets | closed_unassigned_datasets).distinct()

        closed_and_assigned_to_user = Q(published=True) & Q(closed_dataset=True) & Q(users=user)
        closed_and_assigned_to_group = Q(published=True) & Q(closed_dataset=True) & Q(atlas_groups__in=user.atlas_groups.all())

        return self.filter(open_datasets | closed_unassigned_datasets | closed_and_assigned_to_user | closed_and_assigned_to_group).distinct()


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


class Source(models.Model):
    title = models.CharField('Titel', max_length=128, null=True)
    url = models.URLField()
    authenticate = models.BooleanField('Verstuur authenticatieinformatie naar bron', default=False,
                                       help_text='Configureer dit alleen voor vertrouwde bronnen')

    class Meta:
        verbose_name = 'Bron'
        verbose_name_plural = 'Bronnen'

    def __str__(self):
        return f"{self.title}"


class Layer(models.Model):
    SOURCE_WMS_WFS = 'WMS_WFS'
    SOURCE_WMS = 'WMS'
    SOURCE_WFS = 'WFS'
    SOURCE_WMTS = 'WMTS'
    SOURCE_XYZ = 'XYZ'
    SOURCE_MVT = 'MVT'
    SOURCE_TYPES = [
        (SOURCE_WMS_WFS, 'WMS en WFS'),
        (SOURCE_WMS, 'WMS'),
        (SOURCE_WFS, 'WFS'),
        (SOURCE_WMTS, 'WMTS'),
        (SOURCE_XYZ, 'XYZ'),
        (SOURCE_MVT, 'MVT')
    ]

    FORMAT_PNG = 'image/png'
    FORMAT_JPEG = 'image/jpeg'
    FORMAT_JPEG_PNG = 'image/vnd.jpeg-png'
    FORMAT_TYPES = [
        (FORMAT_PNG, 'image/png'),
        (FORMAT_JPEG, 'image/jpeg'),
        (FORMAT_JPEG_PNG, 'image/vnd.jpeg-png'),
    ]

    objects = models.Manager()
    authorized = LayerManager()

    layer_id = models.CharField(
        'Kort kenmerk', max_length=128, null=True, default='',
        help_text='Een uniek kenmerk voor de laag in Atlas. Dit kenmerk komt terug in links naar de laag.')
    title = models.CharField('Titel', max_length=128, null=True)
    layer_name = models.CharField(
        'Laagnaam', max_length=128, null=True, help_text='De naam van de laag op de geoserver.')

    layer_source = models.ForeignKey('Source', verbose_name='Bron', on_delete=models.SET_NULL, null=True)

    format = models.CharField('Formaat', max_length=128, choices=FORMAT_TYPES, default=FORMAT_PNG)

    meta_name = models.CharField('Naam', max_length=128, null=True,)
    meta_description = models.TextField('Omschrijving', null=True,
                                 help_text='Het is mogelijk om tekst op te maken met Markdown in dit veld')
    meta_org = models.CharField('Organisatie', max_length=128, null=True,
                                help_text='Het is mogelijk om tekst op te maken met Markdown in dit veld')
    meta_updated = models.CharField(
        'Laatst bijgewerkt', max_length=128, null=True, help_text='Het is mogelijk om tekst op te maken met Markdown in dit veld')
    meta_link = models.URLField(
        'Meer informatie', max_length=200, blank=True, null=True, help_text='Link naar metadatacatalogus met meer informatie')


    opacity = models.DecimalField(
        'Transparantie', max_digits=1, decimal_places=1, default=0.9)
    visible = models.BooleanField('Zichtbaar', default=False)

    style = models.JSONField(
        'Stijl', default=dict, help_text='Stijl voor een WFS laag in GeoStyler formaat', blank=True, null=True)

    layer_type = models.ForeignKey(
        Category, verbose_name='Categorie', on_delete=models.SET_NULL,
        blank=True, null=True)

    isqueryable = models.BooleanField('Kan doorzocht worden', default=True,
                                      help_text='Deze instelling is alleen van toepassing op Atlas versie 2 en wordt binnenkort verwijderd')

    _popup_attributes = models.CharField(
        'Voer één veld per regel in. Bij geen invoer worden alle velden getoond', max_length=500, blank=True, null=True)

    _search_fields = models.CharField(
        'Zoek in deze velden', max_length=500, blank=True, null=True)

    projection = models.CharField(
        'Projectie', max_length=100, default='EPSG:28992')

    server_type = models.CharField(
        'Servertype', max_length=50, default='geoserver')

    closed_dataset = models.BooleanField(
        'Alleen intern zichtbaar', default=True, help_text='Laag is alleen zichtbaar binnen interne omgeving.')

    login_required = models.BooleanField(
        'Vereis inlog voor deze dataset', default=False, help_text='Voor deze dataset is een inlog vereist.')

    published = models.BooleanField('Gepubliceerd', default=False)

    source_type = models.CharField('Brontype', choices=SOURCE_TYPES, default=SOURCE_WMS_WFS, max_length=20,
                                   help_text='"WMS en WFS" en WFS is zichtbaar in zowel het datapaneel als op de kaart. WMS en WMTS toont alleen op de kaart.'
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

    extent_min_x = models.FloatField(
        'Bereik minimum x', blank=True, default=None, null=True,
        help_text='Vul in om de laag inactief te maken wanneer de weergave buiten het bereik ligt.')
    extent_min_y = models.FloatField(
        'Bereik minimum y', blank=True, default=None, null=True)
    extent_max_x = models.FloatField(
        'Bereik maximum x', blank=True, default=None, null=True)
    extent_max_y = models.FloatField(
        'Bereik maximum y', blank=True, default=None, null=True)

    zoom_min = models.IntegerField(
        'Zoomniveau minimum', blank=True, default=None, null=True,
        help_text='Vul in om de laag inactief te maken wanneer de weergave buiten het zoomniveau ligt.')
    zoom_max = models.IntegerField(
        'Zoomniveau maximum', blank=True, default=None, null=True)

    def __str__(self):
        return self.title

    @property
    def popup_attributes(self):
        attributes = self._popup_attributes
        if not attributes:
            return ""
        result = []
        for attr in attributes.split():
            result.append(f"'{attr}'")
        return f"popupAttributes: [{', '.join(result)}]"

    @property
    def search_fields(self):
        search_fields = self._search_fields
        if not search_fields:
            return ""
        result = []
        for attr in search_fields.split():
            result.append(f"'{attr}'")
        return f"search_fields: [{', '.join(result)}]"

    @property
    def slddiv(self):
        return f"sld_div_{self.layer_id}"

    @property
    def layer_type_str(self):
        return 'themelayer:true'

    @property
    def infodiv(self):
        return f"info_{self.layer_id}"

    @property
    def sld(self):
        return f"sld_{self.layer_id}"

    @property
    def legend(self):
        return f"lgn_{self.layer_id}"

    @property
    def filterid(self):
        return f"flt_{self.layer_id}"

    @property
    def filterdataid(self):
        return f"data_{self.layer_id}"

    @property
    def datazoekid(self):
        return f"zoek_data_{self.layer_id}"

    @property
    def params(self):
        return f"{{'layers': '{self.layer_name}'}}"

    @property
    def source(self):
        # TODO: check server_type case.

        return f"""
source: new ol.source.TileWMS({{
    projection: '{self.projection}',
    url: '{self.url}',
    params: {self.params},
    serverType: '{self.server_type}'
}})"""

    @property
    def is_published(self):
        return self.published

    @property
    def is_closed_dataset(self):
        return self.closed_dataset

    @property
    def extent(self):
        value = [
            self.extent_min_x,
            self.extent_min_y,
            self.extent_max_x,
            self.extent_max_y
        ]

        if all(v is not None for v in value):
            return value

        return None

    @property
    def url(self):
        return self.layer_source.url if self.layer_source else ''

    def to_dict(self):
        return {
            'id': self.layer_id,
            'internal_id': self.id,
            'source_type': self.source_type,
            'title': self.title,
            'name': self.layer_name,
            'opacity': float(self.opacity),
            'style': self.style,
            'url': self.url,
            'server_type': self.server_type,
            'is_base': self.is_base,
            'is_visible': self.is_visible,
            'login_required': self.login_required,
            'projection': self.projection,
            'extent': self.extent,
            'format': self.format,
            'zoom_min': self.zoom_min,
            'zoom_max': self.zoom_max,
            'source': {
                'authenticate': self.layer_source.authenticate if self.layer_source else False
            },
            'category': {
                'id': self.layer_type.id,
                'title': self.layer_type.title
            } if self.layer_type else None,
            'display_properties': self._popup_attributes.split('\r\n') if self._popup_attributes else [],
            'search_properties': self._search_fields.split('\r\n') if self._search_fields else [],
            'metadata': {
                'description': self.meta_description,
                'organization': self.meta_org,
                'updated': self.meta_updated,
                'link': self.meta_link
            },
            'linked_data': [item.to_dict() for item in self.linked_data.all()],
            'templates': [item.to_dict() for item in self.templates.all()]
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
    url = models.CharField(_('URL'), max_length=500)
    source_key = models.CharField(_('Bronsleutel'), max_length=128)
    target_key = models.CharField(_('Doelsleutel'), max_length=128)
    popup_attributes = models.CharField(_('Toon deze velden'), max_length=250, blank=True, null=True,
                                        help_text='Voer één veld per regel in. Bij geen invoer worden alle velden getoond.')
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


class Template(models.Model):
    layer = models.ForeignKey(
        Layer, on_delete=models.CASCADE, related_name='templates')

    source = models.ForeignKey('Source', on_delete=models.CASCADE)
    endpoint = models.CharField(_('Endpoint'), max_length=500)
    title = models.CharField('Titel', max_length=128)
    list = models.CharField(_('Tabel Veld met lijst'), max_length=128, blank=True, null=True)
    headers = models.TextField(_('Tabel kopjes'), max_length=128, blank=True, null=True,
                               help_text='Voer één veld per regel in.')
    fields = models.TextField(_('Tabel velden'), blank=True, null=True,
                              help_text='Voer één veld per regel in.')
    template = models.TextField(_('Vrij veld template'), blank=True, null=True, help_text='Het is mogelijk om Markdown te gebruiken.')
    ordering = models.PositiveIntegerField('Sortering',
                                           default=0, editable=True, db_index=True)


    class Meta:
        verbose_name = 'Template'
        verbose_name_plural = 'Templates'
        ordering = ['ordering']

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            'source': {
                'authenticate': self.source.authenticate,
                'url': self.source.url
            },
            'endpoint': self.endpoint,
            'title': self.title,
            'list': self.list,
            'headers': self.headers.split('\r\n') if self.headers else [],
            'fields': self.fields.split('\r\n') if self.fields else [],
            'template': self.template
        }


class Map(models.Model):
    title = models.CharField('Titel', max_length=128, null=True)
    slug = AutoSlugField('Kort kenmerk', blank=True, populate_from='title', editable=True,
                         help_text='Een uniek kort kenmerk voor de kaart in Atlas. Dit kenmerk komt terug in links naar het thema.')
    layers = models.ManyToManyField(Layer, verbose_name='Lagen', blank=True)
    features = models.JSONField(default=dict, blank=True, verbose_name='Functies')
    settings = models.JSONField(default=dict, blank=True, verbose_name='Instellingen')

    def get_absolute_url(self):
        return reverse('homepage:v3', args=[self.slug]) + '/'

    class Meta:
        verbose_name = 'Kaart'
        verbose_name_plural = 'Kaarten'
        ordering = ['title']

    def __str__(self):
        return f"{self.title}"


def validate_file_extension(value):
    ext = path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.svg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class ViewerVisibleManager(models.Manager):
    def for_request(self, request):
        if is_ctrix(request) or request.user.is_authenticated:
            return self.get_queryset()

        return self.get_queryset().filter(models.Q(internal=False))

class Viewer(models.Model):
    TYPE_GOOGLE_MAPS = 'GOOGLE_MAPS'
    TYPE_STREET_SMART = 'STREET_SMART'
    TYPE_OBLIQUO = 'OBLIQUO'
    VIEWER_TYPES = [
        (TYPE_GOOGLE_MAPS, 'Google Maps'),
        (TYPE_STREET_SMART, 'Street Smart'),
        (TYPE_OBLIQUO, 'Obliquo'),
    ]

    ordering = models.PositiveIntegerField('Sortering', default=0, editable=True, db_index=True)
    label = models.CharField(max_length=128)
    type = models.CharField('Type', choices=VIEWER_TYPES, default=TYPE_GOOGLE_MAPS, max_length=20)
    username = models.CharField(null=True, blank=True, max_length=128)
    password = models.CharField(null=True, blank=True, max_length=128)
    api_key = models.CharField(null=True, blank=True, max_length=128)
    url = models.CharField(null=True, blank=True, max_length=255)
    internal = models.BooleanField('Alleen intern zichtbaar', default=True,
                                   help_text='Is alleen zichtbaar binnen interne omgeving. Hou er rekening mee dat de gebruikernaam, '
                                   'het wachtwoord of de API key gedeeld wordt met het publieke internet op het moment dat deze optie uit staat.')

    objects = models.Manager()
    visible = ViewerVisibleManager()


    class Meta:
        verbose_name = 'Viewer'
        verbose_name_plural = 'Viewers'
        ordering = ['ordering', 'label']

    def __str__(self):
        return self.label

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label,
            'type': self.type,
            'username': self.username,
            'password': self.password,
            'api_key': self.api_key,
            'url': self.url
        }
