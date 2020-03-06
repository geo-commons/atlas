from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import JSONField


class SavedDataset(models.Model):

    title = models.CharField('title', max_length=128, null=True)
    json = JSONField()

    saved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    created_at = models.DateTimeField('created_at', auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True)

    def __str__(self):
        return f'{self.title} saved by: {self.saved_by}'

    class Meta:
        ordering = ('-created_at', '-title')

    @property
    def number_of_records(self):
        json_data = self.json
        try:
            return json_data['numberReturned']
        except KeyError:
            return None
