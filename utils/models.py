from django.db import models


class BaseModel(models.Model):

    created_at = models.DateTimeField('created_at', auto_now_add=True)
    updated_at = models.DateTimeField('created_at', auto_now=True)

    pubplished = models.BooleanField('status', default=False)

    def __str__(self):
        return f'{self.__class__.title} ({self.__class__.title})'

    def is_active(self):
        return self.status

    class Meta:
        abstract = True
