from django.test import Client, TestCase
from django.urls import reverse

from webservice.models import Category, Layer


class TestHomePageExcludeThemeLayers(TestCase):
    def test_exclude_excluded_layers(self):
        self.client = Client()

        Layer.objects.create(
            layer_id="purm_stembureaus_2018",
            title="Stembureaus",
            layer_name="topp:Purm_Stembureaus_2018",
            closed_dataset=False,
            published=True,
            not_in_atlas=True,
            layer_type=Category.objects.create(
                title='thema_layer'))

        Layer.objects.create(
            layer_id="purm_stembureaus_2019",
            title="Stembureaus",
            layer_name="topp:Purm_Stembureaus_2019",
            closed_dataset=False,
            published=True,
            not_in_atlas=False,
            layer_type=Category.objects.create(
                title='thema_layer'))

        response = self.client.get(reverse('homepage:homepage'))
        self.assertContains(response, 'purm_stembureaus_2019')
        self.assertNotContains(response, 'purm_stembureaus_2018')
