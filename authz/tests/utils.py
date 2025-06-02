from webservice.tests.utils import create_test_source
from authz.models import Authorization

def create_test_authorization(resource_name="testlayername"):
    authorization, created = Authorization.objects.get_or_create(
        source=create_test_source(),
        resource=resource_name,
    )

    return authorization