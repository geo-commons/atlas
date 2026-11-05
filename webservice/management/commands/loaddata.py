from django.core.management import call_command
from django.core.management.commands.loaddata import Command as DjangoLoadDataCommand


AUDITED_MODELS = (
    "authz.authorization",
    "table.table",
    "table.tabletotable",
    "table.layertotable",
    "tables.table",
    "user_management.atlasgroup",
    "user_management.atlasuser",
    "webservice.category",
    "webservice.source",
    "webservice.metadataset",
    "webservice.layer",
    "webservice.map",
    "webservice.mapcategory",
    "webservice.maplayer",
    "webservice.viewer",
)


class Command(DjangoLoadDataCommand):
    """Load fixtures and create their initial audit history."""

    def handle(self, *fixture_labels, **options):
        output = super().handle(*fixture_labels, **options)
        call_command("populate_history", *AUDITED_MODELS, verbosity=options["verbosity"])
        return output
