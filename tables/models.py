from django.db import models
from django_extensions.db.fields import AutoSlugField


class TableManager(models.Manager):
    def for_request(self, request):
        if request.user.is_anonymous:
            return self.filter(login_required=False)

        return self.all()


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
                         help_text='Een uniek kort kenmerk voor tabel.')

    source = models.ForeignKey('webservice.Source', on_delete=models.CASCADE)
    endpoint = models.CharField('Endpoint', max_length=500)
    method = models.CharField('Methode', choices=METHOD_TYPES, max_length=20)

    list_query = models.CharField('Veldnaam van lijst',
                                  max_length=128, blank=True, null=True)

    list_headings = models.TextField(
        'Kopjes in lijstweergave', blank=True, null=True)

    list_fields = models.TextField(
        'Velden in lijstweergave', blank=True, null=True)

    search_fields = models.JSONField(
        'Velden waarop gezocht kan worden', blank=True, default=list)

    login_required = models.BooleanField(
        'Vereis inlog voor deze tabel', default=False, help_text='De tabel is alleen zichtbaar voor ingelogde gebruikers.')

    ordering = models.PositiveIntegerField('Sortering',
                                           default=0, editable=True, db_index=True)

    created_at = models.DateTimeField('created_at', auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True)

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
            'source': {
                'authenticate': self.source.authenticate,
                'url': self.source.url
            },
            'endpoint': self.endpoint,
            'method': self.method,
            'list_query': self.list_query,
            'list_headings': self.list_headings.split('\r\n') if self.list_headings else [],
            'list_fields': self.list_fields.split('\r\n') if self.list_fields else [],
            'search_fields': self.search_fields,
            'login_required': self.login_required,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
