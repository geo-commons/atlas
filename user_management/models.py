from django.db import models
from django.contrib.auth.models import AbstractUser


class AtlasGroup(models.Model):
    name = models.CharField('Groep', max_length=50)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Groep'
        verbose_name_plural = 'Groepen'

class AtlasUser(AbstractUser):
    atlas_groups = models.ManyToManyField(AtlasGroup, blank=True)
