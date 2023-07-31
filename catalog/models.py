from django.db import models
from django_extensions.db.fields import AutoSlugField


class Topic(models.Model):
    title = models.CharField('Titel', max_length=256)
    slug = AutoSlugField('Kort kenmerk', blank=False, unique=True, populate_from='title', editable=True,
                         help_text='Een uniek kort kenmerk.')

    class Meta:
        verbose_name = 'Onderwerp'
        verbose_name_plural = 'Onderwerpen'
        ordering = ['title']

    def __str__(self):
        return self.title


class Dataset(models.Model):
    title = models.CharField('Titel', max_length=256)
    slug = AutoSlugField('Kort kenmerk', blank=False, unique=True, populate_from='title', editable=True,
                         help_text='Een uniek kort kenmerk.')

    abstract = models.TextField('Samenvatting', blank=True, null=True)

    data_owner = models.CharField(
        'Data eigenaar', max_length=256, blank=True, null=True)
    data_administrator = models.CharField(
        'Data beheerder', max_length=256, blank=True, null=True)

    contact_phone = models.CharField(
        'Telefoon', max_length=256, blank=True, null=True)
    contact_address = models.CharField(
        'Adres', max_length=256, blank=True, null=True)
    contact_email = models.CharField(
        'E-mail', max_length=256, blank=True, null=True)

    update_frequency = models.TextField(
        'Update frequentie', blank=True, null=True)

    created_at = models.DateTimeField('Aanmaakdatum')
    updated_at = models.DateTimeField('Laatst gewijzigd')

    topics = models.ManyToManyField('Topic', verbose_name='Onderwerpen')

    map_layers = models.ManyToManyField(
        'webservice.Layer', verbose_name='Kaartlagen', blank=True)

    class Meta:
        verbose_name = 'Dataset'
        verbose_name_plural = 'Datasets'
        ordering = ['title']

    def __str__(self):
        return self.title
