from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from user_management.models import AtlasGroup, AtlasUser
from webservice.models import Layer, Category


@override_settings(CTRIX_IPS='0.0.0.0')
class TestHomePageAnonymousUser(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_button(self):
        response = self.client.get(reverse('homepage:homepage'))
        self.assertNotContains(response, 'loginmodal')

    def test_added_to_layerlist(self):
        Layer.objects.create(
            layer_id="purm_stembureaus_2018",
            title="Stembureaus",
            layer_name="topp:Purm_Stembureaus_2018",
            closed_dataset=False,
            published=True,
            layer_type=Category.objects.create(
                title='base_registration'))
        Layer.objects.create(
            layer_id="purm_stembureaus_2017",
            title="Stembureaus",
            layer_name="topp:Purm_Stembureaus_2017",
            closed_dataset=True,
            published=True,
            layer_type=Category.objects.create(
                title='base_registration'))
        response = self.client.get(reverse('homepage:homepage'))
        self.assertContains(response, 'purm_stembureaus_2018')
        self.assertNotContains(response, 'purm_stembureaus_2017')


@override_settings(CTRIX_IPS='0.0.0.0')
class TestHomePageAnonymousUserCtrix(TestCase):
    def setUp(self):
        cred = {'username': 'testuser', 'password': '1234'}
        user = AtlasUser(**cred)
        user.save()
        group = AtlasGroup(name="stembureaus")
        group.save()

        self.client = Client(REMOTE_ADDR=settings.CTRIX_IPS[0])
        Layer.objects.create(
            layer_id="purm_stembureaus_2018",
            title="Stembureaus",
            layer_name="topp:Purm_Stembureaus_2018",
            closed_dataset=False,
            layer_type=Category.objects.create(
                title='thema_layer'),
            published=True)

        Layer.objects.create(
            layer_id="purm_stembureaus_2017",
            title="Stembureaus",
            layer_name="topp:Purm_Stembureaus_2017",
            closed_dataset=True,
            layer_type=Category.objects.create(
                title='thema_layer'),
            published=True)

        closed_with_user = Layer.objects.create(
            layer_id="purm_stembureaus_2016",
            title="Stembureaus",
            layer_name="topp:Purm_Stembureaus_2016",
            closed_dataset=True,
            layer_type=Category.objects.create(
                title='thema_layer'),
            published=True)

        closed_with_user.save()
        closed_with_user.users.add(user)
        closed_with_user.save()

        closed_with_group = Layer.objects.create(
            layer_id="purm_stembureaus_2015",
            title="Stembureaus",
            layer_name="topp:Purm_Stembureaus_2015",
            closed_dataset=True,
            layer_type=Category.objects.create(
                title='thema_layer'),
            published=True)

        closed_with_group.save()
        closed_with_group.atlas_groups.add(group)
        closed_with_group.save()

    def test_login_button(self):
        response = self.client.get(reverse('homepage:homepage'))
        self.assertContains(response, 'loginmodal')

    def test_added_to_layerlist(self):
        response = self.client.get(reverse('homepage:homepage'))
        self.assertContains(response, 'purm_stembureaus_2018')
        self.assertContains(response, 'purm_stembureaus_2017')
        self.assertNotContains(response, 'purm_stembureaus_2016')
        self.assertNotContains(response, 'purm_stembureaus_2015')

        self.assertEqual(len(Layer.objects.all()), 4)


@override_settings(CTRIX_IPS='0.0.0.0')
class TestHomePageUserPermissions(TestCase):

    cred = {'username': 'testuser', 'password': '1234'}

    @classmethod
    def setUpTestData(cls):
        user = AtlasUser(**cls.cred)
        user.save()
        layer_1 = Layer(
            layer_id="purm_stembureaus_2018",
            title="Stembureaus",
            layer_name="topp:Purm_Stembureaus_2018",
            closed_dataset=True,
            layer_type=Category.objects.create(
                title='thema_layer'),
            published=True)
        layer_1.save()
        layer_1.users.add(user)
        layer_1.save()

    def setUp(self):
        self.client = Client(REMOTE_ADDR=settings.CTRIX_IPS[0])
        self.client.force_login(
            user=AtlasUser.objects.get(username='testuser'))

    def test_login_button(self):
        response = self.client.get(reverse('homepage:homepage'))
        self.assertNotContains(response, 'loginmodal')

    def test_logout_button(self):
        response = self.client.get(reverse('homepage:homepage'))
        self.assertContains(response, 'logout')

    def test_added_to_layerlist(self):
        response = self.client.get(reverse('homepage:homepage'))
        self.assertContains(response, 'purm_stembureaus_2018')


@override_settings(CTRIX_IPS='0.0.0.0')
class TestHomePageGroupPermissions(TestCase):

    cred = {'username': 'testuser', 'password': '1234'}

    @classmethod
    def setUpTestData(cls):
        group = AtlasGroup(name="stembureaus")
        group.save()
        user = AtlasUser(**cls.cred)
        user.save()
        user.atlas_groups.add(group)
        layer_1 = Layer(
            layer_id="purm_stembureaus_2018",
            title="Stembureaus",
            layer_name="topp:Purm_Stembureaus_2018",
            closed_dataset=True,
            layer_type=Category.objects.create(
                title='thema_layer'),
            published=True)
        layer_1.save()
        layer_1.atlas_groups.add(group)
        layer_1.save()

    def setUp(self):
        self.client = Client(REMOTE_ADDR=settings.CTRIX_IPS[0])
        self.client.force_login(
            user=AtlasUser.objects.get(username='testuser'))

    def test_login_button(self):
        response = self.client.get(reverse('homepage:homepage'))
        self.assertNotContains(response, 'loginmodal')

    def test_logout_button(self):
        response = self.client.get(reverse('homepage:homepage'))
        self.assertContains(response, 'logout')

    def test_added_to_layerlist(self):
        response = self.client.get(reverse('homepage:homepage'))
        self.assertContains(response, 'purm_stembureaus_2018')

    def test_with_extra_public_layer(self):
        Layer(
            layer_id="purm_stembureaus_2017",
            title="Stembureaus2017",
            layer_name="topp:Purm_Stembureaus_2017",
            closed_dataset=False,
            layer_type=Category.objects.create(
                title='thema_layer'),
            published=True).save()
        response = self.client.get(reverse('homepage:homepage'))
        self.assertContains(response, 'purm_stembureaus_2018')
        self.assertContains(response, 'purm_stembureaus_2017')
