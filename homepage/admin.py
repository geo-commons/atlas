from django.contrib import admin

from .models import SavedDataset

admin.site.register(SavedDataset, admin.ModelAdmin)
