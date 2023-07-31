from django.contrib import admin
from catalog.models import Topic, Dataset
from catalog.admin import TopicAdmin, DatasetAdmin


class CatalogAdminSite(admin.AdminSite):
    site_header = 'Catalogus beheer'
    site_title = 'Catalogus beheer'
    site_url = '/catalog'


site = CatalogAdminSite(name='catalog_admin')
site.register(Topic, TopicAdmin)
site.register(Dataset, DatasetAdmin)
