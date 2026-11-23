import importlib

from django.test import TestCase


migration = importlib.import_module('webservice.migrations.0162_convert_liquid_replace')


class LiquidReplaceMigrationTest(TestCase):
    def test_converts_replace_calls_in_nested_template_values(self):
        value = {
            'endpoint': '/zoeken?postcode={{ postcode | replace(" ", "") }}&test=test',
            'filters': [
                "{{ postcode | replaceAll(' ', '') }}",
                "{{ postcode.replaceAll(' ', '') }}",
            ],
            'plain_text': 'replace(" ", "")',
        }

        converted = migration.convert_legacy_replace_in_value(value)

        self.assertEqual(converted['endpoint'], '/zoeken?postcode={{ postcode | replace: " ", "" }}&test=test')
        self.assertEqual(converted['filters'], [
            "{{ postcode | replace: ' ', '' }}",
            "{{ postcode | replace: ' ', '' }}",
        ])
        self.assertEqual(converted['plain_text'], value['plain_text'])
        self.assertEqual(migration.convert_legacy_replace_in_value(converted), converted)
