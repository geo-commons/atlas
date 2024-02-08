from django.db import models

from utils.tools import is_internal


class Authorization(models.Model):
    source = models.ForeignKey('webservice.Source', on_delete=models.CASCADE)
    ordering = models.PositiveIntegerField('Sortering',
                                           default=0, editable=True, db_index=True)

    resource = models.CharField(
        max_length=255, null=True, blank=True, help_text='Naam van de laag of de resource')

    description = models.CharField(
        max_length=255, help_text='Een beschrijvende tekst voor beheerders')

    login_required = models.BooleanField(
        'Vereis inlog van gebruiker', default=True)
    only_internal = models.BooleanField(
        'Alleen intern zichtbaar', default=True, help_text='Alleen zichtbaar binnen interne omgeving.')

    audit_log = models.BooleanField(
        default=True, help_text='Voeg verzoeken toe aan de audit log')
    atlas_groups = models.ManyToManyField('user_management.AtlasGroup', blank=True, verbose_name='Groepen',
                                          help_text='De inhoud van dit endpoint kan alleen bekeken worden als de gebruiker lid is van een van deze groepen.')
    response_filter = models.TextField(
        null=True, blank=True, help_text='Voeg een jq filter toe om een data response te filteren, in het geval van WMS GetFeatureInfo, WFS GetFeature en REST')

    class Meta:
        verbose_name = 'Autorisatie'
        verbose_name_plural = 'Autorisaties'
        ordering = ('source', 'resource', 'ordering')

    def __str__(self):
        return self.resource

    def is_accessible_by(self, user, request):
        if not is_internal(request):
            if self.only_internal:
                return False

        if not user.is_authenticated:
            if not self.login_required and not self.atlas_groups.exists():
                return True

            return False

        if not self.atlas_groups.exists():
            return True

        user_groups = list(user.atlas_groups.all())
        return any(group for group in self.atlas_groups.all() if group in user_groups)


class Log(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    ip = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    resource = models.CharField(max_length=255, null=True, blank=True)
    params = models.JSONField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
        ordering = ['-time_created']

    def __str__(self):
        return str(self.id)
