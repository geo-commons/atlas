from django import forms
from django.contrib.postgres.forms import JSONField


class UploadDatasetForm(forms.Form):
    title = forms.CharField(label='Titel', max_length=128)
    json = JSONField(label='JSON')
