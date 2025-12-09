import uuid
from os import path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django_extensions.db.fields import AutoSlugField

from user_management.models import AtlasGroup
from utils.tools import is_internal
from webservice.util import safe_float_or_null


class LayerManager(models.Manager):
    def for_request(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            return self.distinct()

        query = Q(published=True)

        if not request.user.is_authenticated and settings.SHOW_LAYERS_ONLY_WHEN_ACCESSIBLE:
            query &= Q(login_required=False)

        if not is_internal(request):
            query &= Q(closed_dataset=False)

        if request.user.is_authenticated:
            query &= Q(atlas_groups__in=request.user.atlas_groups.all()) | Q(
                atlas_groups=None)
        else:
            query &= Q(atlas_groups=None)

        return self.filter(query).distinct()


class Category(models.Model):
    objects = models.Manager()

    # MBS (https://gitlab.com/purmerend/datalab/mbs) depends on this field
    # so inform them when changing.
    title = models.CharField('Titel', max_length=128, null=True)

    slug = AutoSlugField('Kort kenmerk', default=None, blank=False, unique=True, populate_from='title',
                         overwrite_on_add=False, editable=True,
                         help_text='Een uniek kort kenmerk voor de categorie in Atlas.', max_length=255)

    ordering = models.PositiveIntegerField('Sortering',
                                           default=0, editable=True, db_index=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categorieën'
        ordering = ['ordering', 'title']


class Source(models.Model):
    SOURCE_OWS = 'OWS'
    SOURCE_WMTS = 'WMTS'
    SOURCE_REST = 'REST'

    SOURCE_TYPES = [
        (SOURCE_OWS, 'OWS'),
        (SOURCE_WMTS, 'WMTS'),
        (SOURCE_REST, 'REST'),
    ]

    title = models.CharField('Titel', max_length=128, null=True)
    slug = AutoSlugField('Kort kenmerk', null=True, default=None, blank=False, unique=True, populate_from='title',
                         editable=True,
                         help_text='Een uniek kort kenmerk voor de bron in Atlas.', max_length=255)

    source_type = models.CharField('Brontype', choices=SOURCE_TYPES, default=SOURCE_OWS, max_length=20,
                                   help_text='Selecteer het type bron')

    url = models.URLField()

    login_required = models.BooleanField(
        'Vereis inlog voor deze bron', default=False,
        help_text='De inhoud van deze bron kan alleen bekeken worden door ingelogde gebruikers.')

    atlas_groups = models.ManyToManyField(
        AtlasGroup, blank=True, verbose_name='Groepen',
        help_text='De inhoud van deze dataset kan alleen bekeken worden als de gebruiker lid is van een van deze groepen.')

    authenticate = models.BooleanField('Verstuur authenticatieinformatie naar bron', default=False,
                                       help_text='Configureer dit alleen voor vertrouwde bronnen')

    class Meta:
        verbose_name = 'Bron'
        verbose_name_plural = 'Bronnen'
        ordering = ['title']

    def __str__(self):
        return f"{self.title}"


class Theme(models.Model):
    title = models.CharField('Naam', max_length=128, null=False)
    slug = models.SlugField('Kort kenmerk', null=False, unique=True,
                            help_text='Een uniek kort kenmerk voor het Thema in Atlas', editable=True)

    class Meta:
        verbose_name = 'Theme'
        verbose_name_plural = 'Themes'
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class DatasetManager(models.Manager):
    def for_request(self, request):
        if request.user.is_anonymous:
            return self.filter(published=True, show_in_overview=True)

        if request.user.is_authenticated and request.user.is_superuser:
            return self.all()

        return self.filter(published=True)


class Dataset(models.Model):
    objects = models.Manager()
    authorized = DatasetManager()

    title = models.CharField('Naam', max_length=128,
                             help_text="De naam van de dataset")
    slug = models.SlugField('Kort kenmerk', null=False, unique=True,
                            help_text='Een uniek kort kenmerk voor de Dataset in Atlas', editable=True)
    description = models.TextField(
        'Beschrijving', null=True, help_text="Het is mogelijk om tekst op te maken met Markdown in dit veld",
        blank=True)
    source_description = models.TextField(
        'Bron omschrijving', null=True,
        help_text="Beschrijft de herkomst van de dataset. Het is mogelijk om tekst op te maken met Markdown in dit veld",
        blank=True)
    organization = models.CharField(
        'Organisatie', max_length=128, null=True, blank=True)
    contact = models.CharField(
        'Contactpersoon', max_length=128, null=True, blank=True)
    data_owner = models.CharField(
        'Eigenaar van de data', max_length=128, null=True, blank=True)
    data_controller = models.CharField(
        'Data beheerder', max_length=128, null=True, blank=True)
    last_updated = models.DateTimeField(
        'Laatste update', null=True, blank=True)
    update_frequency = models.CharField(
        'Update hoeveelheid', max_length=128, null=True, blank=True)
    purpose_of_manufacture = models.CharField(
        'Doel van de vervaardiging', max_length=128, null=True, blank=True)
    themes = models.ManyToManyField(Theme, related_name='datasets')
    dataset_category = models.ForeignKey(
        Category, verbose_name='Categorie', on_delete=models.SET_NULL,
        blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to='thumbnails/',
        blank=True,
        null=True,
        help_text="Selecteer een afbeelding om als thumbnail te gebruiken"
    )

    published = models.BooleanField('Gepubliceerd',
                                    help_text="Markeer dit veld als Gepubliceerd om de dataset te publiceren en beschikbaar te maken voor andere gebruikers. Zet dit veld uit om de dataset te bewaren als concept en nog niet beschikbaar te maken voor andere gebruikers.",
                                    default=False)
    show_in_overview = models.BooleanField('Toon in overzicht weergave',
                                           help_text="Schakel dit veld in om de dataset weer te geven in het overzicht van het dataportaal. Laat het uitgeschakeld om de dataset te verbergen in het overzicht, zelfs als deze gepubliceerd is.",
                                           default=True)

    class Meta:
        verbose_name = 'Dataset'
        verbose_name_plural = 'Datasets'
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class MetadatasetManager(models.Manager):
    def for_request(self, request):
        if request.user.is_anonymous:
            return self.filter(status='completed')

        if request.user.is_authenticated and request.user.is_superuser:
            return self.all()

        return self.filter(status='completed')


class TopicCategory(models.TextChoices):
    FARMING = "farming", _("Landbouw en Veeteelt")
    BIOTA = "biota", _("Biodiversiteit en Ecologie")
    BOUNDARIES = "boundaries", _("Grenzen en Administratie")
    CLIMATOLOGY_METEOROLOGY_ATMOSPHERE = "climatologyMeteorologyAtmosphere", _("Klimaat en Meteorologie")
    ECONOMY = "economy", _("Economie en Werkgelegenheid")
    ELEVATION = "elevation", _("Hoogte en Reliëf")
    ENVIRONMENT = "environment", _("Milieu en Natuurbescherming")
    GEOSCIENTIFIC_INFORMATION = "geoscientificInformation", _("Geowetenschappen")
    HEALTH = "health", _("Gezondheid en Veiligheid")
    IMAGERY_BASE_MAPS_EARTH_COVER = "imageryBaseMapsEarthCover", _("Basiskaarten en Beeldmateriaal")
    INTELLIGENCE_MILITARY = "intelligenceMilitary", _("Defensie en Militaire Zaken")
    INLAND_WATERS = "inlandWaters", _("Binnenwateren")
    LOCATION = "location", _("Locatie en Adressering")
    OCEANS = "oceans", _("Oceanen en Kustgebieden")
    PLANNING_CADASTRE = "planningCadastre", _("Ruimtelijke Ordening en Kadaster")
    SOCIETY = "society", _("Maatschappij en Cultuur")
    STRUCTURE = "structure", _("Bouwwerken en Infrastructuur")
    TRANSPORTATION = "transportation", _("Transport en Vervoer")
    UTILITIES_COMMUNICATION = "utilitiesCommunication", _("Nutsvoorzieningen en Communicatie")


class RoleType(models.TextChoices):
    RESOURCE_PROVIDER = "resourceProvider", _("Data verstrekker")
    CUSTODIAN = "custodian", _("Beheerder")
    OWNER = "owner", _("Eigenaar")
    USER = "user", _("Gebruiker")
    DISTRIBUTOR = "distributor", _("Distributeur")
    ORIGINATOR = "originator", _("Maker")
    POINT_OF_CONTACT = "pointOfContact", _("Contactpunt")
    PRINCIPAL_INVESTIGATOR = "principalInvestigator", _("Onderzoeksleider")
    PROCESSOR = "processor", _("Bewerker")
    PUBLISHER = "publisher", _("Uitgever")
    AUTHOR = "author", _("Auteur")


class UpdateMethodType(models.TextChoices):
    MANUAL = "manual", _("Manueel")
    AUTOMATIC = "automatic", _("Automatisch (via API)")


class AuthorizationLevelType(models.TextChoices):
    OPEN_DATA = "open_data", _("Open data")
    INTERNAL = "internal", _("Interne toegang")
    EXTERNAL = "external", _("Externe toegang")
    PROTECTED = "protected", _("Beveiligd")


class StatusType(models.TextChoices):
    COMPLETED = "completed", _("Gepubliceerd")
    UNDER_DEVELOPMENT = "underDevelopment", _("In ontwikkeling")
    HISTORICAL_ARCHIVE = "historicalArchive", _("Gearchiveerd")


class AccessConstraintsType(models.TextChoices):
    LICENSE = "license", _("Licentie")
    INTELLECTUAL_PROPERTY = "intellectualPropertyRights", _("Intellectuele eigendomsrechten")
    RESTRICTED = "restricted", _("Beperkt")
    OTHER = "otherRestrictions", _("Overige beperkingen")


class OtherConstraintsType(models.TextChoices):
    PUBLICDOMAIN_MARK = "publicdomain-mark", _("Open data (publiek)")
    PUBLICDOMAIN_ZERO = "publicdomain-zero", _("Open data (CC0)")
    LICENSES_BY = "licenses-by", _("Open data (CC-BY)")
    LICENSES_BY_SA = "licenses-by-sa", _("Open data (CC-BY-SA)")
    LICENSES_BY_NC = "licenses-by-nc", _("Open data (CC-BY-NC)")
    LICENSES_BY_NC_SA = "licenses-by-nc-sa", _("Gebruiksvoorwaarden (CC-by-nc-sa)")
    LICENSES_BY_ND = "licenses-by-nd", _("Gebruiksvoorwaarden (CC-by-nd)")
    LICENSES_BY_NC_ND = "licenses-by-nc-nd", _("Gebruiksvoorwaarden (CC-by-nc-nd)")
    CUSTOM = "custom", _("Gebruiksvoorwaarden Geogedeeld")


class Metadataset(models.Model):
    objects = models.Manager()
    authorized = MetadatasetManager()

    title = models.CharField('Naam', max_length=128,
                             help_text="De naam van de dataset")

    slug = AutoSlugField('Kort kenmerk', null=True, default=None, blank=False, unique=True, populate_from='title',
                         overwrite_on_add=False, editable=True,
                         help_text='Een uniek kort kenmerk voor de metadataset in Atlas. Gebruik alleen kleine letters, cijfers en afbreekstreepjes.',
                         max_length=255)

    description = models.TextField(
        'Beschrijving', null=True, help_text="Het is mogelijk om tekst op te maken met Markdown in dit veld",
        blank=True)

    abstract = models.TextField(
        'Toelichting dataset', null=True, blank=True,
        help_text="Een beschrijving van de inhoud van de dataset, geef in deze samenvatting  publieks vriendelijk informatie over de inhoud van de dataset. Deze is minimaal drie zinnen en maximaal één alinea lang (2000 karakters).")

    topic_category = models.CharField(
        'Onderwerp', max_length=128, null=True, blank=True, choices=TopicCategory.choices,
        help_text="Het belangrijkste onderwerp van de dataset.")

    keyword = models.CharField(
        'Trefwoord', max_length=500, null=True, blank=True,
        help_text="In het algemeen gebruikte woorden of geformaliseerde zinnen om een dataset of datasetserie te beschrijven. Eén trefwoord per regel.")

    statement = models.TextField(
        'Doel van de vervaardiging', null=True, blank=True, help_text="De reden waarom de dataset is gemaakt.")

    source_origin = models.TextField(
        'Oorspronkelijke bron', null=True, blank=True,
        help_text="Algemene beschrijving herkomst. Dit is de bron waar de dataset vandaan komt, dat kan een URL zijn of een beschrijving van de bron.")

    source_location = models.TextField(
        'Bronlocatie', null=True, blank=True, help_text="Bijvoorbeeld Objectstore (COG), S3, etc.")

    source_email_internal = models.EmailField(
        'E-mailadres aanspreekpunt', null=True, blank=True,
        help_text="Het e-mailadres van het intern aanspreekpunt van de bron.")

    source_organization = models.CharField(
        'Verantwoordelijke organisatie', max_length=128, null=True, blank=True,
        help_text="De organisatie van de verantwoordelijke van de bron, bijvoorbeeld de gemeente, provincie, Nederlandse organisatie voor toegepast-natuurwetenschappelijk onderzoek (TNO), etc.")

    source_email_public = models.EmailField(
        'E-mailadres verantwoordelijke', null=True, blank=True,
        help_text="Het e-mailadres van de verantwoordelijke organisatie van de bron.")

    source_email_person_responsible = models.EmailField(
        'E-mailadres verantwoordelijke', null=True, blank=True,
        help_text="Het e-mailadres van de verantwoordelijke van de bron.")

    source_role_person_responsible = models.CharField(
        'Rol verantwoordelijke', max_length=128, null=True, blank=True, choices=RoleType.choices,
        help_text="De rol van de verantwoordelijke van de bron.")

    update_method = models.CharField(
        'Updatemethode', max_length=128, null=True, blank=True, choices=UpdateMethodType.choices,
        help_text="De methode waarmee de dataset wordt bijgewerkt.", default="manual")

    update_frequency = models.CharField(
        'Updatefrequentie', max_length=128, null=True, blank=True,
        help_text="De frequentie waarmee de dataset wordt bijgewerkt.")

    last_updated = models.DateField(
        'Laatst bijgewerkt', null=True, blank=True,
        help_text="De datum waarop de dataset voor het laatst is bijgewerkt.")

    authorization_level = models.CharField(
        'Autorisatieniveau', max_length=128, null=True, blank=True, choices=AuthorizationLevelType.choices,
        help_text="Het niveau van autorisatie voor de dataset.")

    status = models.CharField(
        'Status', max_length=128, null=True, blank=True, choices=StatusType.choices,
        help_text="De status van de dataset.", default="underDevelopment")

    show_in_overview = models.BooleanField(
        'Toon in dataportaal', default=False, help_text="Toon de dataset in het dataportaal.")

    access_constraints = models.CharField(
        'Juridische toegangsrestricties', max_length=128, null=True, blank=True, choices=AccessConstraintsType.choices,
        help_text="De juridische toegangsrestricties van de dataset.")

    other_constraints = models.CharField(
        'Overige beperkingen', max_length=128, null=True, blank=True, choices=OtherConstraintsType.choices,
        help_text="De overige beperkingen van de dataset.")

    usage_constraints = models.TextField(
        'Gebruiksbeperkingen', null=True, blank=True,
        help_text="In dit veld geef je aan waarvoor de dataset niet mag of kan worden gebruikt. Bijvoorbeeld: Niet gebruiken voor navigatie.")

    meta_email_internal = models.EmailField(
        'E-mailadres aanspreekpunt', null=True, blank=True,
        help_text="Het e-mailadres van het intern aanspreekpunt van de verantwoordelijke van de metadata.")

    meta_organization = models.CharField(
        'Organisatie', max_length=128, null=True, blank=True,
        help_text="De naam van de organisatie verantwoordelijk voor de metadata. Gebruik de volledig uitgeschreven naam van de verantwoordelijke organisatie. Bijvoorbeeld: Gemeente Purmerend.")

    meta_email_person_responsible = models.EmailField(
        'E-mailadres verantwoordelijke', null=True, blank=True,
        help_text="Het e-mailadres van de organisatie verantwoordelijk voor de metadata. Gebruik bij voorkeur een functioneel e-mailadres.")

    meta_role_person_responsible = models.CharField(
        'Rol verantwoordelijke', max_length=128, null=True, blank=True, choices=RoleType.choices,
        help_text="De rol van de verantwoordelijke van de bron.")

    class Meta:
        verbose_name = 'Metadataset'
        verbose_name_plural = 'Metadatasets'
        ordering = ['title']

    def __str__(self):
        return self.title


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

    # MBS (https://gitlab.com/purmerend/datalab/mbs) depends on this field
    # so inform them when changing.
    slug = AutoSlugField('Kort kenmerk', null=True, default=None, blank=False, unique=True, populate_from='title',
                         overwrite_on_add=False, editable=True,
                         help_text='Een uniek kenmerk voor de laag in Atlas. Dit kenmerk komt terug in links naar de laag.)',
                         max_length=255)

    title = models.CharField('Titel', max_length=128, null=True)

    description = models.TextField('Beschrijving', blank=True, null=True,
                                   help_text='Beschrijving van de kaartlaag. Het is mogelijk om tekst op te maken met Markdown in dit veld.')

    # MBS (https://gitlab.com/purmerend/datalab/mbs) depends on this field
    # so inform them when changing.
    layer_name = models.CharField(
        'Laagnaam', max_length=128, null=True, help_text='De naam van de laag op de geoserver.')

    layer_source = models.ForeignKey(
        'Source', verbose_name='Bron', on_delete=models.SET_NULL, null=True)

    format = models.CharField(
        'Formaat', max_length=128, choices=FORMAT_TYPES, default=FORMAT_PNG)

    # MBS (https://gitlab.com/purmerend/datalab/mbs) depends on the meta_* fields
    # so inform them when changing.
    meta_name = models.CharField(
        'Naam', max_length=128, blank=True, null=True, )
    meta_description = models.TextField('Omschrijving', blank=True, null=True,
                                        help_text='Het is mogelijk om tekst op te maken met Markdown in dit veld')
    meta_lineage = models.TextField('Bron', blank=True, null=True,
                                    help_text='Beschrijft de herkomst van de dataset. Het is mogelijk om tekst op te maken met Markdown in dit veld')
    meta_org = models.CharField('Organisatie', max_length=128, blank=True, null=True,
                                help_text='Het is mogelijk om tekst op te maken met Markdown in dit veld')
    meta_contact = models.CharField(
        'Contactpersoon', max_length=200, blank=True, null=True)
    meta_updated = models.CharField(
        'Laatst bijgewerkt', max_length=128, blank=True, null=True,
        help_text='Het is mogelijk om tekst op te maken met Markdown in dit veld')
    meta_link = models.URLField(
        'Meer informatie', max_length=200, blank=True, null=True,
        help_text='Link naar metadatacatalogus met meer informatie')

    opacity = models.DecimalField(
        'Transparantie', max_digits=2, decimal_places=1, default=0.9,
        validators=[MinValueValidator(0), MaxValueValidator(1)])
    visible = models.BooleanField('Zichtbaar', default=False)

    server_style = models.CharField(
        'Stijlnaam voor WMS / WMTS laag', max_length=128, blank=True, null=True,
        help_text='Stijlnaam zoals beschikbaar op de server')

    client_style = models.JSONField(
        'Stijl voor WFS / MVT laag', default=dict, help_text='Stijl in GeoStyler formaat', blank=True, null=True)

    friendly_fields = models.JSONField(
        'Vriendelijke veldnamen', default=dict, help_text='Maak veldnamen vriendelijk', blank=True, null=True)

    templated_properties = models.JSONField(
        'Templatevelden', default=dict, help_text='Velden die samengesteld worden vanuit een template', blank=True,
        null=True)

    layer_type = models.ForeignKey(
        Category, verbose_name='Categorie', on_delete=models.SET_NULL,
        blank=True, null=True)

    _popup_attributes = models.TextField(
        'Voer één veld per regel in. Bij geen invoer worden alle velden getoond', blank=True, null=True)

    _search_fields = models.CharField(
        'Zoek in deze velden', max_length=500, blank=True, null=True)

    _search_terms = models.CharField(
        'Zoektermen', max_length=500, blank=True, null=True,
        help_text='Deze worden gebruikt om de laag beter vindbaar te maken in het lagenpaneel. Voer één zoekterm per regel in.')

    # MBS (https://gitlab.com/purmerend/datalab/mbs) depends on this field
    # so inform them when changing.
    projection = models.CharField(
        'Projectie', max_length=100, default='EPSG:28992')

    server_type = models.CharField(
        'Servertype', max_length=50, default='geoserver')

    closed_dataset = models.BooleanField(
        'Alleen intern zichtbaar', default=True, help_text='Laag is alleen zichtbaar binnen interne omgeving.')

    login_required = models.BooleanField(
        'Vereis inlog voor deze dataset', default=False,
        help_text='De inhoud van deze dataset kan alleen bekeken worden door ingelogde gebruikers.')

    authenticated_can_mutate = models.BooleanField('Ingelogde gebruikers kunnen kaartlaag muteren', default=False,
                                                   help_text="Alle ingelogde gebruikers kunnen wanneer deze optie aanstaat kaartlagen muteren")

    published = models.BooleanField('Gepubliceerd', default=False)

    is_exportable = models.BooleanField('Kaartlaag is exporteerbaar', default=True)

    source_type = models.CharField('Brontype', choices=SOURCE_TYPES, default=SOURCE_WMS_WFS, max_length=20,
                                   help_text='"WMS en WFS" en WFS is zichtbaar in zowel het datapaneel als op de kaart. WMS en WMTS toont alleen op de kaart.'
                                   )

    legend_url = models.URLField(
        'Legenda', help_text='Overschrijf link naar legenda', blank=True, null=True, max_length=1000)

    is_base = models.BooleanField('Is basislaag', default=False)
    is_visible = models.BooleanField('Is standaard zichtbaar', default=False)
    is_selectable = models.BooleanField('Is selecteerbaar', default=True)
    use_html_info_format = models.BooleanField(
        'Haal detailinformatie als HTML op bij de bron', default=False)
    show_in_detail_panel = models.BooleanField(
        'Toon laag in detail- en dataweergave', default=True)
    is_filterable_in_legend = models.BooleanField(
        'Laag is filterbaar in legenda', default=False)

    not_in_atlas = models.BooleanField(
        'Toon laag alleen in een themakaart',
        default=False,
        help_text='De laag wordt niet getoond in de standaardkaart')

    atlas_groups = models.ManyToManyField(
        AtlasGroup, blank=True, verbose_name='Groepen',
        help_text='De inhoud van deze dataset kan alleen bekeken worden als de gebruiker lid is van een van deze groepen.')

    atlas_write_groups = models.ManyToManyField(
        AtlasGroup, blank=True, verbose_name='Groepen', related_name='atlas_write_groups',
        help_text='De inhoud van deze dataset kan alleen gemuteerd worden als de gebruiker lid is van een van deze groepen.')

    created_at = models.DateTimeField('created_at', auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True)

    ordering = models.PositiveIntegerField('Sortering',
                                           default=0, editable=True, db_index=True)

    extent_min_x = models.DecimalField(
        'Bereik minimum x', blank=True, default=None, null=True, max_digits=10, decimal_places=2,
        help_text='Vul in om de laag inactief te maken wanneer de weergave buiten het bereik ligt.')
    extent_min_y = models.DecimalField(
        'Bereik minimum y', blank=True, default=None, null=True, max_digits=10, decimal_places=2)
    extent_max_x = models.DecimalField(
        'Bereik maximum x', blank=True, default=None, null=True, max_digits=10, decimal_places=2)
    extent_max_y = models.DecimalField(
        'Bereik maximum y', blank=True, default=None, null=True, max_digits=10, decimal_places=2)

    zoom_min = models.DecimalField(
        'Zoomniveau minimum', blank=True, default=None, null=True, max_digits=5, decimal_places=2,
        help_text='Vul in om de laag inactief te maken wanneer de weergave buiten het zoomniveau ligt.')
    zoom_max = models.DecimalField(
        'Zoomniveau maximum', blank=True, default=None, null=True, max_digits=5, decimal_places=2)

    dataset = models.ForeignKey(
        Dataset, on_delete=models.SET_NULL, null=True, related_name="layers", blank=True)

    metadataset = models.ForeignKey(
        Metadataset, on_delete=models.SET_NULL, null=True, related_name="layers", blank=True)

    def __str__(self):
        return self.title

    @property
    def popup_attributes(self):
        return self._popup_attributes.split('\r\n') if self._popup_attributes else []

    @property
    def search_fields(self):
        return self._search_fields.split('\r\n') if self._search_fields else []

    @property
    def search_terms(self):
        return self._search_terms.split('\r\n') if self._search_terms else []

    @property
    def slddiv(self):
        return f"sld_div_{self.slug}"

    @property
    def layer_type_str(self):
        return 'themelayer:true'

    @property
    def infodiv(self):
        return f"info_{self.slug}"

    @property
    def sld(self):
        return f"sld_{self.slug}"

    @property
    def legend(self):
        return f"lgn_{self.slug}"

    @property
    def filterid(self):
        return f"flt_{self.slug}"

    @property
    def filterdataid(self):
        return f"data_{self.slug}"

    @property
    def datazoekid(self):
        return f"zoek_data_{self.slug}"

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

    def is_accessible_by(self, user, request):
        if not is_internal(request):
            if self.closed_dataset:
                return False

        if not user.is_authenticated:
            if not self.login_required and not self.atlas_groups.exists():
                return True

            return False

        if not self.atlas_groups.exists():
            return True

        user_groups = list(user.atlas_groups.all())
        return any(group for group in self.atlas_groups.all() if group in user_groups)

    def is_mutable_by(self, user, request):
        if not is_internal(request) and self.closed_dataset:
            return False

        if not user.is_authenticated:
            return False

        if self.authenticated_can_mutate:
            return True

        if not self.atlas_write_groups.exists():
            return False

        user_groups = list(user.atlas_groups.all())
        return any(group for group in self.atlas_write_groups.all() if group in user_groups)

    def to_dict(self, user, request):
        return {
            'id': self.slug,
            'internal_id': self.id,
            'source_type': self.source_type,
            'title': self.title,
            'description': self.description,
            'name': self.layer_name,
            'opacity': float(self.opacity),
            'server_style': self.server_style,
            'client_style': self.client_style,
            'friendly_fields': self.friendly_fields,
            'templated_properties': self.templated_properties,
            'url': self.url,
            'server_type': self.server_type,
            'is_base': self.is_base,
            'is_visible': self.is_visible,
            'is_selectable': self.is_selectable,
            'use_html_info_format': self.use_html_info_format,
            'show_in_detail_panel': self.show_in_detail_panel,
            'login_required': self.login_required,
            'projection': self.projection,
            'extent': self.extent,
            'format': self.format,
            'zoom_min': safe_float_or_null(self.zoom_min),
            'zoom_max': safe_float_or_null(self.zoom_max),
            'source': {
                'authenticate': self.layer_source.authenticate if self.layer_source else False
            },
            'category': {
                'id': self.layer_type.id,
                'title': self.layer_type.title
            } if self.layer_type else None,
            'display_properties': self._popup_attributes.split('\r\n') if self._popup_attributes else [],
            'search_properties': self._search_fields.split('\r\n') if self._search_fields else [],
            'search_terms': self._search_terms.split('\r\n') if self._search_terms else [],
            'metadata': {
                'description': self.meta_description,
                'lineage': self.meta_lineage,
                'organization': self.meta_org,
                'contact': self.meta_contact,
                'updated': self.meta_updated,
                'link': self.meta_link
            },
            'metadataset': {
                'id': self.metadataset.id,
                'title': self.metadataset.title,
                'abstract': self.metadataset.abstract,
                'topic_category': self.metadataset.topic_category,
                'keyword': self.metadataset.keyword,
                'statement': self.metadataset.statement,
                'source_origin': self.metadataset.source_origin,
                'source_organization': self.metadataset.source_organization,
                'source_email_public': self.metadataset.source_email_public,
                'source_role_person_responsible': self.metadataset.source_role_person_responsible,
                'update_frequency': self.metadataset.update_frequency,
                'last_updated': self.metadataset.last_updated.strftime(
                    '%d-%m-%Y') if self.metadataset.last_updated else None,
                'status': self.metadataset.status,
                'access_constraints': self.metadataset.access_constraints,
                'other_constraints': self.metadataset.other_constraints,
                'usage_constraints': self.metadataset.usage_constraints,
                'meta_organization': self.metadataset.meta_organization,
                'meta_email_person_responsible': self.metadataset.meta_email_person_responsible,
                'meta_role_person_responsible': self.metadataset.meta_role_person_responsible,
            } if self.metadataset else None,
            'linked_data': [item.to_dict() for item in self.linked_data.all()],
            'templates': [item.to_dict() for item in self.templates.all()],
            'legend_url': self.legend_url,
            'is_filterable_in_legend': self.is_filterable_in_legend,
            'can_write': self.is_mutable_by(user, request),
            'is_exportable': self.is_exportable
        }

    class Meta:
        verbose_name = 'Kaartlaag'
        verbose_name_plural = 'Kaartlagen'
        ordering = ['layer_type__ordering', 'ordering', 'title']


class LinkedData(models.Model):
    source = models.ForeignKey(
        Layer, on_delete=models.CASCADE, related_name='linked_data')

    title = models.CharField(_('Titel'), max_length=128, null=True)
    layer_name = models.CharField(_('Laag naam'), max_length=128)
    url = models.CharField(_('URL'), max_length=500)
    source_key = models.CharField(_('Bronsleutel'), max_length=128)
    target_key = models.CharField(_('Doelsleutel'), max_length=128)

    headers = models.TextField(_('Tabel kopjes'), max_length=250, blank=True, null=True,
                               help_text='Voer één veld per regel in.')
    popup_attributes = models.TextField(_('Tabel velden'), max_length=250, blank=True, null=True,
                                        help_text='Voer één veld per regel in. Bij geen invoer worden alle velden getoond.')
    use_detail_view = models.BooleanField(
        'Gebruik detailweergave', default=False)
    detail_view_fields = models.TextField(_('Detailweergave velden'), max_length=250, blank=True, null=True,
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
            'headers': self.headers.split('\r\n') if self.headers else [],
            'display_properties': self.popup_attributes.split('\r\n') if self.popup_attributes else [],
            'use_detail_view': self.use_detail_view,
        }


class Template(models.Model):
    METHOD_GET = 'GET'
    METHOD_POST = 'POST'

    METHOD_TYPES = [
        (METHOD_GET, 'GET'),
        (METHOD_POST, 'POST'),
    ]

    layer = models.ForeignKey(
        Layer, on_delete=models.CASCADE, related_name='templates')

    source = models.ForeignKey('Source', on_delete=models.CASCADE)
    endpoint = models.CharField(_('Endpoint'), max_length=500)
    method = models.CharField(
        'Methode', choices=METHOD_TYPES, max_length=20, default=METHOD_GET)
    title = models.CharField('Titel', max_length=128)
    list = models.CharField(_('Tabel Veld met lijst'),
                            max_length=128, blank=True, null=True)
    headers = models.TextField(_('Tabel kopjes'), max_length=128, blank=True, null=True,
                               help_text='Voer één veld per regel in.')
    fields = models.TextField(_('Tabel velden'), blank=True, null=True,
                              help_text='Voer één veld per regel in.')
    template = models.TextField(_('Vrij veld template'), blank=True,
                                null=True, help_text='Het is mogelijk om Markdown te gebruiken.')
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
            'method': self.method,
            'title': self.title,
            'list': self.list,
            'headers': self.headers.split('\r\n') if self.headers else [],
            'fields': self.fields.split('\r\n') if self.fields else [],
            'template': self.template
        }


class SelectionManager(models.Manager):
    def for_request(self, request):
        if request.user.is_anonymous:
            return self.filter(login_required=False)

        return self.all()


# TODO: Remove Selections, this is not used anymore in Atlas
class Selection(models.Model):
    objects = models.Manager()
    authorized = SelectionManager()

    title = models.CharField('Titel', max_length=128, null=True)
    slug = AutoSlugField('Kort kenmerk', blank=True, unique=True, populate_from='title', editable=True,
                         help_text='Een uniek kort kenmerk voor de kaartselectie in Atlas.', max_length=255)

    layers = models.ManyToManyField(Layer, verbose_name='Lagen', blank=True)

    login_required = models.BooleanField(
        'Vereis inlog voor deze selectie', default=False,
        help_text='De selectie kan alleen bekeken worden door ingelogde gebruikers.')

    class Meta:
        verbose_name = 'Selectie'
        verbose_name_plural = 'Selecties'

    def __str__(self):
        return self.title


class MapLayer(models.Model):
    layer = models.ForeignKey(
        'Layer', on_delete=models.CASCADE, related_name='maps_layer')
    map = models.ForeignKey(
        'Map', on_delete=models.CASCADE, related_name='map_layers')
    settings = models.JSONField()

    class Meta:
        verbose_name = 'Kaartlaag'
        verbose_name_plural = 'Kaartlagen'
        ordering = ['layer__layer_type__ordering', 'layer__ordering', 'layer__title']
        constraints = [
            models.UniqueConstraint(fields=["layer", "map"], name='unique_map_layer'),
        ]

    def __str__(self):
        return f"{self.map} - {self.layer}"

    def to_dict(self):
        return {
            'layer': self.layer.id,
            'settings': self.settings
        }


class MapManager(models.Manager):
    def for_request(self, request):
        if request.user.is_anonymous:
            return self.filter(published=True, show_in_overview=True)

        if request.user.is_authenticated and request.user.is_superuser:
            return self.all()

        return self.filter(published=True)


class Map(models.Model):
    objects = models.Manager()
    authorized = MapManager()

    title = models.CharField('Titel', max_length=128, null=True)
    slug = AutoSlugField('Kort kenmerk', blank=True, unique=True, populate_from='title', editable=True,
                         help_text='Een uniek kort kenmerk voor de kaart in Atlas.', max_length=255)

    old_layers = models.ManyToManyField(
        Layer, verbose_name='Lagen', blank=True, related_name='old_layers')
    layers = models.ManyToManyField(
        Layer, verbose_name='Lagen', blank=True, through='MapLayer')

    features = models.JSONField(
        default=dict, blank=True, verbose_name='Functies')
    settings = models.JSONField(
        default=dict, blank=True, verbose_name='Instellingen')

    login_required = models.BooleanField(
        'Vereis inlog voor deze kaart', default=False,
        help_text='De inhoud van deze kaart kan alleen bekeken worden door ingelogde gebruikers.')

    thumbnail = models.ImageField(
        upload_to='thumbnails/',
        blank=True,
        null=True,
        help_text="Selecteer een afbeelding om als thumbnail te gebruiken"
    )

    description = models.TextField(
        'Beschrijving van de kaart', null=True,
        help_text="Het is mogelijk om tekst op te maken met Markdown in dit veld", blank=True)

    about = models.TextField(
        'Beschrijving van de kaart voor de zijbalk', null=True,
        help_text="Het is mogelijk om tekst op te maken met Markdown in dit veld", blank=True)

    about_title = models.CharField(
        'Titel van de zijbalk', null=True, max_length=128,
        help_text="De titel van de zijbalk die gebruikt wordt in de zijbalkinformatie", blank=True)

    published = models.BooleanField('Gepubliceerd',
                                    help_text="Markeer dit veld als Gepubliceerd om de kaart te publiceren en beschikbaar te maken voor andere gebruikers. Zet dit veld uit om de kaart te bewaren als concept en nog niet beschikbaar te maken voor andere gebruikers.",
                                    default=False)
    show_in_overview = models.BooleanField('Toon in overzicht weergave',
                                           help_text="Schakel dit veld in om de kaart weer te geven in het overzicht van het dataportaal. Laat het uitgeschakeld om de kaart te verbergen in het overzicht, zelfs als deze gepubliceerd is.",
                                           default=True)

    def get_absolute_url(self):
        return reverse('homepage:v3', args=[self.slug]) + '/'

    class Meta:
        verbose_name = 'Kaart'
        verbose_name_plural = 'Kaarten'
        ordering = ['title']

    def __str__(self):
        return f"{self.title}"

    def to_dict(self):
        return {
            'title': self.title,
            'slug': self.slug,
            'layers': [layer.to_dict() for layer in self.map_layers.all()],
            'features': self.features,
            'settings': self.settings,
            'about': self.about,
            'about_title': self.about_title,
            'thumbnail': self.thumbnail.url if self.thumbnail else None
        }


def validate_file_extension(value):
    ext = path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.svg']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class ViewerVisibleManager(models.Manager):
    def for_request(self, request):
        if is_internal(request) or request.user.is_authenticated:
            return self.get_queryset()

        return self.get_queryset().filter(models.Q(internal=False))


class Viewer(models.Model):
    TYPE_GOOGLE_MAPS = 'GOOGLE_MAPS'
    TYPE_STREET_SMART = 'STREET_SMART'
    TYPE_OBLIQUO = 'OBLIQUO'
    TYPE_IFRAME = 'IFRAME'
    TYPE_BUTTON = 'BUTTON'
    VIEWER_TYPES = [
        (TYPE_GOOGLE_MAPS, 'Google Maps'),
        (TYPE_STREET_SMART, 'Street Smart'),
        (TYPE_OBLIQUO, 'Obliquo'),
        (TYPE_IFRAME, 'Iframe'),
        (TYPE_BUTTON, 'Knop naar nieuw tabblad'),
    ]

    ordering = models.PositiveIntegerField(
        'Sortering', default=0, editable=True, db_index=True)
    label = models.CharField(max_length=128)
    type = models.CharField('Type', choices=VIEWER_TYPES,
                            default=TYPE_GOOGLE_MAPS, max_length=20)
    username = models.CharField(null=True, blank=True, max_length=128)
    password = models.CharField(null=True, blank=True, max_length=128)
    api_key = models.CharField(null=True, blank=True, max_length=128)
    url = models.CharField(null=True, blank=True, max_length=255)
    is_oblique = models.BooleanField(default=False, blank=True)
    internal = models.BooleanField('Alleen zichtbaar voor ingelogde gebruikers en interne omgeving', default=True,
                                   help_text='Hou er rekening mee dat de gebruikernaam, het wachtwoord of de API key gedeeld wordt met het publieke internet op het moment dat deze optie uit staat.')

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
            'is_oblique': self.is_oblique,
            'url': self.url
        }


class Drawing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    features = models.JSONField()

    class Meta:
        verbose_name = 'Tekening'
        verbose_name_plural = 'Tekeningen'

    def __str__(self):
        return str(self.id)
