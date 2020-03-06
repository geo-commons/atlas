import csv
import json
import os
from datetime import datetime
from io import StringIO

from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from homepage.forms import UploadDatasetForm
from homepage.models import SavedDataset
from user_management.models import AtlasUser


def load_and_read_testjson(filename, client):
    with open(os.path.join(os.path.dirname(__file__), filename)) as fp:

        features = fp.read()

    data = {'title': 'test123', 'json': features}
    client.post(reverse('homepage:savedataset'), data)
    pk = SavedDataset.objects.all()[0].pk
    response = client.get(
        reverse(
            'homepage:save_dataset_view', kwargs={
                'pk': pk,
                'type_': 'csv'
            }))
    data = response.content.decode('UTF-8')
    csvdata = StringIO(data)
    reader = csv.reader(csvdata)

    return [row for row in reader]


class TestSaveDatasetsForm(TestCase):
    """Testing the save datasets form."""

    def test_save_valid_json_string(self):
        form_data = {'title': 'Dataset', 'json': '{"test": "test"}'}
        form = UploadDatasetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_save_valid_json_list(self):
        form_data = {'title': 'Dataset', 'json': '{"test": [1, 3, 4]}'}
        form = UploadDatasetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_save_invalid_json_list(self):
        form_data = {'title': 'Dataset', 'json': "test"}
        form = UploadDatasetForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_save_no_json_list(self):
        form_data = {
            'title': 'Dataset',
        }
        form = UploadDatasetForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestSavedDatasetAnonymous(TestCase):
    def setUp(self):
        self.client = Client()

    def test_download_page(self):
        """Downloads page is not accessable outside the CTRIX environment. """

        response = self.client.get(reverse('homepage:downloads'))
        self.assertEqual(response.status_code, 403)


class TestSavedDataset(TestCase):
    def setUp(self):
        self.client = Client(REMOTE_ADDR=settings.CTRIX_IPS[0])
        cred = {'username': 'testuser', 'password': '1234'}
        self.user = AtlasUser(**cred)
        self.user.save()

    def test_title(self):
        """Title is generated from timestamp and title given by frontend."""

        json_data = json.dumps({'test': '[1, 2, 3, 4]'})
        now = datetime.now().strftime('%Y%m%d')

        data = {'title': 'test', 'json': json_data}

        response = self.client.post(reverse('homepage:savedataset'), data)
        self.assertRedirects(response, reverse('homepage:downloads'))
        dataset = SavedDataset.objects.all()[0]
        self.assertRegex(dataset.title, '{}\d{{4}}-test'.format(now))

    def test_save_user(self):
        """If user is logged in, the user is also saved on the SavedDataset."""
        self.client.force_login(
            user=AtlasUser.objects.get(username='testuser'))
        json_data = json.dumps({'test': '[1, 2, 3, 4]'})

        data = {'title': 'test', 'json': json_data}
        self.client.post(reverse('homepage:savedataset'), data)

        dataset = SavedDataset.objects.all()[0]
        self.assertEqual(dataset.saved_by, self.user)

    def test_save_single_entry_json(self):
        """Saved json with one feature, gives one row output + headers."""
        rows = load_and_read_testjson('features.json', self.client)
        self.assertEqual(len(rows), 2)  # Headers and rows

    def test_save_multiple_entries_json(self):
        """Saved json with more feature, gives saved rows output + headers."""
        rows = load_and_read_testjson('multiple_features.json', self.client)
        self.assertEqual(len(rows), 3)  # Headers and rows
