from django.contrib.auth import get_user_model
from django.test import RequestFactory
from rest_framework.test import APITestCase

from webservice.models import Metadataset
from webservice.tests.utils import create_test_layer


class TestMetadatasetFmeScriptApi(APITestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123',
        )
        self.metadataset = Metadataset.objects.create(
            title="FME Test Dataset",
            status="completed",
            fme_script="batch/update.fmw",
        )
        self.layer = create_test_layer(title="FME Test Layer")
        self.layer.metadataset = self.metadataset
        self.layer.published = True
        self.layer.save()

    def test_fme_script_roundtrip_via_metadataset_api(self):
        self.client.force_authenticate(self.admin_user)
        url = f"/atlas/api/v1/metadatasets/{self.metadataset.id}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["fme_script"], "batch/update.fmw")

        response = self.client.patch(url, {"fme_script": "other/workspace.fmw"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["fme_script"], "other/workspace.fmw")
        self.metadataset.refresh_from_db()
        self.assertEqual(self.metadataset.fme_script, "other/workspace.fmw")

    def test_layer_detail_returns_metadataset_id_without_fme_script(self):
        self.client.force_authenticate(self.admin_user)
        response = self.client.get(f"/atlas/api/v1/layers/{self.layer.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["metadataset"], self.metadataset.id)

    def test_layer_list_excludes_fme_script(self):
        self.client.force_authenticate(self.admin_user)
        response = self.client.get("/atlas/api/v1/layers/")

        self.assertEqual(response.status_code, 200)
        layer_result = next(item for item in response.data["results"] if item["id"] == self.layer.id)
        self.assertIsNotNone(layer_result["metadataset"])
        self.assertNotIn("fme_script", layer_result["metadataset"])

    def test_public_metadataset_excludes_fme_script(self):
        response = self.client.get(f"/atlas/api/v1/metadatasets/{self.metadataset.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("fme_script", response.data)

    def test_layer_to_dict_excludes_fme_script(self):
        request = RequestFactory().get("/")
        request.user = self.admin_user

        layer_data = self.layer.to_dict(self.admin_user, request)

        self.assertIsNotNone(layer_data["metadataset"])
        self.assertNotIn("fme_script", layer_data["metadataset"])
