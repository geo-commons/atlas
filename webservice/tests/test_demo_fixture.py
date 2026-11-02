from django.core.management import call_command
from django.test import TestCase

from webservice.models import Layer, Map, Source


class DemoFixtureTests(TestCase):
    def test_loads_without_system_data_conflicts(self):
        call_command("loaddata", "data/demo.json")

        self.assertTrue(Source.objects.exists())
        self.assertTrue(Layer.objects.exists())
        self.assertTrue(Map.objects.exists())
