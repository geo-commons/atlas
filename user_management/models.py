from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import AbstractUser


class AtlasGroup(models.Model):
    name = models.CharField('Groep', max_length=50)
    external_id = models.CharField(
        'External ID', max_length=255, null=True, blank=True, help_text='Het unieke kernmerk van de groep in de inlogbron.')
    slug = AutoSlugField('Kort kenmerk', null=True, blank=True, unique=True, populate_from='name', editable=True,
                         help_text='Een uniek kort kenmerk voor de groep.')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Groep'
        verbose_name_plural = 'Groepen'


class AtlasUser(AbstractUser):
    name = models.CharField(
        'Volledige naam', max_length=255, blank=True, null=True)
    external_id = models.CharField(
        'External ID', max_length=255, editable=False, null=True, blank=True, help_text='Het unieke kernmerk van de gebruiker in de inlogbron.'
    )

    atlas_groups = models.ManyToManyField(
        AtlasGroup, blank=True, related_name='atlas_users')

    def __str__(self):
        return self.username
