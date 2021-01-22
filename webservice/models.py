from django.conf import settings
from django.db import models
from django.urls import reverse
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


class CategoryManager(models.Manager):
    def environment(self, ctrix=True):
        if ctrix:
            return self.all()

        return self.filter(closed_theme=False)


class Category(models.Model):
    objects = models.Manager()
    environment_dependent = CategoryManager()

    title = models.CharField('title', max_length=128, null=True)

    slug = AutoSlugField(blank=False, populate_from='title', overwrite=True)
    js_type = models.CharField(
        'Javascript type',
        max_length=128,
        default='themelayer:true',
        help_text='javascript...')

    closed_theme = models.BooleanField('Gesloten thema', default=True)
    ordering = models.PositiveIntegerField(
        default=0, editable=True, db_index=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categorieën'
        ordering = ['ordering', 'title']


class Layer(models.Model):
    objects = models.Manager()
    authorized = LayerManager()

    layer_id = models.CharField(
        'Layer_id', max_length=128, null=True, default="")
    title = models.CharField('title', max_length=128, null=True)
    layer_name = models.CharField('layer_name', max_length=128, null=True)

    meta_name = models.CharField('meta_naam', max_length=128, null=True)
    meta_kind = models.CharField('meta_soort', max_length=128, null=True)
    meta_org = models.CharField('meta_org', max_length=128, null=True)
    meta_updated = models.CharField(
        'meta_bijgewerkt',
        max_length=128,
        null=True,
        help_text='''
De waarde wordt door javascript geëvalueerd
(Bijv: "01-01-2018", getDate("year"))'
        ''')

    opacity = models.DecimalField(
        'opacity', max_digits=1, decimal_places=1, default=0.9)
    visible = models.BooleanField('visible', default=False)

    layer_type = models.ForeignKey(
        Category, verbose_name='Categorie', on_delete=models.SET_NULL,
        blank=True, null=True)

    isqueryable = models.BooleanField('isqueryable', default=True)

    _popup_attributes = models.CharField(
        'popup attributes', max_length=250, blank=True, null=True)

    _search_fields = models.CharField(
        'Zoek velden', max_length=250, blank=True, null=True)

    projection = models.CharField(
        'projection', max_length=100, default='EPSG:28992')

    url = models.CharField(
        'url',
        max_length=500,
        default='https://datalab.purmerend.nl/geoserver/topp/wms?')

    server_type = models.CharField(
        'Server type', max_length=50, default='geoserver')

    closed_dataset = models.BooleanField('Gesloten data', default=True)

    published = models.BooleanField('Gepubliceerd', default=False)

    not_in_atlas = models.BooleanField(
        'Alleen in een thema, niet in Atlas',
        default=False,
        help_text='''
Kaartlaag wordt niet in Atlas getoond, alleen als kaartlaag in een thema.
        ''')

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='owner')

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    atlas_groups = models.ManyToManyField(AtlasGroup, blank=True)

    created_at = models.DateTimeField('created_at', auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True)

    ordering = models.PositiveIntegerField(
        default=0, editable=True, db_index=True)

    def __str__(self):
        return '{} (Gesloten dataset: {})'.format(
            self.title, self.is_closed_dataset)

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
        """

        if self.layer_type == 'theme_layer':
            return "themelayer:true"
        elif self.layer_type == 'base_registration':
            return "basisreg:true"
        elif self.layer_type == 'base_layer':
            return "isBaseLayer:true"
        """

        return self.layer_type.js_type

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
            'title': self.title,
            'name': self.layer_name,
            'opacity': float(self.opacity),
            'url': self.url,
            'server_type': self.server_type,
            'is_base': False,
            'is_visible': False,
            'category': {
                'id': self.layer_type.id,
                'title': self.layer_type.title
            },
            'display_properties': self._popup_attributes.split('\r\n') if self._popup_attributes else [],
            'search_properties': self._search_fields.split('\r\n') if self._search_fields else []
        }

    class Meta:
        verbose_name = 'Kaartlaag'
        verbose_name_plural = 'Kaartlagen'
        ordering = ['layer_type__ordering', 'layer_type__title', 'ordering', 'title']


class AtlasTheme(models.Model):
    title = models.CharField('title', max_length=128, null=True)

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
