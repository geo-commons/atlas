from django.core.management.base import BaseCommand

from webservice.services.main_map import ensure_main_map


class Command(BaseCommand):
    help = 'Create the default main map when it does not exist yet.'

    def handle(self, *args, **options):
        main_map, created = ensure_main_map()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created main map: {main_map.id} ({main_map.slug})'))
            return

        self.stdout.write(self.style.SUCCESS(f'Main map already exists: {main_map.id} ({main_map.slug})'))
