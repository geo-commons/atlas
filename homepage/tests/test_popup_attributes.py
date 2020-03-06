from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from user_management.models import AtlasGroup, AtlasUser
from webservice.models import Category, Layer


class TestHomePageCategoryPopupAttributes(TestCase):
    def setUp(self):
        self.client = Client()

    def test_without_popup_attributes(self):
        Layer.objects.create(
            layer_id="purm_stembureaus_2018",
            title="Stembureaus",
            layer_name="topp:Purm_Stembureaus_2018",
            closed_dataset=False,
            published=True,
            layer_type=Category.objects.create(
                title='thema_layer', js_type='theme_layer:true'),
            _popup_attributes='')
        response = self.client.get(reverse('homepage:homepage'))
        self.assertNotContains(response, 'popupAttributes')

    def test_with_popup_attributes(self):
        Layer.objects.create(
            layer_id="purm_stembureaus_2018",
            title="Stembureaus",
            layer_name="topp:Purm_Stembureaus_2018",
            closed_dataset=False,
            published=True,
            layer_type=Category.objects.create(
                title='thema_layer',
                closed_theme=False,
                js_type='theme_layer:true'),
            _popup_attributes='test\ntest2 test3')
        response = self.client.get(reverse('homepage:homepage'))
        self.assertContains(response,
                            "popupAttributes: ['test', 'test2', 'test3']", 1)
