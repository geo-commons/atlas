from django.db import models
from django_extensions.db.fields import AutoSlugField

from utils.tools import is_internal


class TableManager(models.Manager):
    def for_request(self, request):
        query = self.all()

        if not is_internal(request):
            query = query.filter(only_internal=False)

        if request.user.is_anonymous:
            query = query.filter(login_required=False)

        return query


class Table(models.Model):
    METHOD_GET = 'GET'
    METHOD_POST = 'POST'

    METHOD_TYPES = [
        (METHOD_GET, 'GET'),
        (METHOD_POST, 'POST'),
    ]

    objects = models.Manager()
    authorized = TableManager()

    title = models.CharField('Titel', max_length=128)
    slug = AutoSlugField('Kort kenmerk', blank=True, unique=True, populate_from='title', editable=True,
                         help_text='Een uniek kort kenmerk voor tabel.', max_length=255)

    source = models.ForeignKey('webservice.Source', on_delete=models.CASCADE)
    endpoint = models.CharField('Endpoint', max_length=500)
    method = models.CharField('Methode', choices=METHOD_TYPES, max_length=20)

    list_query = models.CharField('Veldnaam van lijst',
                                  max_length=128, blank=True, null=True)

    page_attribute = models.CharField('Veldnaam van pagina',
                                  max_length=128, blank=True, null=True)
    items_per_page_attribute = models.CharField('Veldnaam van items per pagina',
                                  max_length=128, blank=True, null=True)
    total_items_page_attribute = models.CharField('Veldnaam van totaal aantal items',
                                  max_length=128, blank=True, null=True)

    error_template = models.CharField(
        'Template van foutmelding', max_length=128, blank=True, null=True)

    list_headings = models.TextField(
        'Kopjes in lijstweergave', blank=True, null=True)

    list_fields = models.TextField(
        'Velden in lijstweergave', blank=True, null=True)

    search_fields = models.JSONField(
        'Velden waarop gezocht kan worden', blank=True, default=list)

    login_required = models.BooleanField(
        'Vereis inlog voor deze tabel', default=False,
        help_text='De tabel is alleen zichtbaar voor ingelogde gebruikers.')
    only_internal = models.BooleanField(
        'Alleen intern zichtbaar', default=True, help_text='Alleen zichtbaar binnen interne omgeving.')

    ordering = models.PositiveIntegerField('Sortering',
                                           default=0, editable=True, db_index=True)

    created_at = models.DateTimeField('created_at', auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True)

    description = models.TextField(
        'Beschrijving van de tabel', null=True,
        help_text="Het is mogelijk om tekst op te maken met Markdown in dit veld", blank=True)

    thumbnail = models.ImageField(
        upload_to='thumbnails/',
        blank=True,
        null=True,
        help_text="Selecteer een afbeelding om als thumbnail te gebruiken"
    )

    class Meta:
        verbose_name = 'Tabel'
        verbose_name_plural = 'Tabellen'
        ordering = ['ordering', 'title']

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            'title': self.title,
            'slug': self.slug,
            'description': self.description,
            'source': {
                'authenticate': self.source.authenticate,
                'url': self.source.url
            },
            'endpoint': self.endpoint,
            'method': self.method,
            'list_query': self.list_query,
            'page_attribute': self.page_attribute,
            'items_per_page_attribute': self.items_per_page_attribute,
            'total_items_page_attribute': self.total_items_page_attribute,
            'list_headings': self.list_headings.split('\r\n') if self.list_headings else [],
            'list_fields': self.list_fields.split('\r\n') if self.list_fields else [],
            'search_fields': self.search_fields,
            'error_template': self.error_template,
            'login_required': self.login_required,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'thumbnail': self.thumbnail.url if self.thumbnail else None
        }
