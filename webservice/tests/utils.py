from user_management.models import AtlasGroup, AtlasUser
from webservice.models import Layer, Source


def create_test_group(group_name="testgroup"):
    group, created = AtlasGroup.objects.get_or_create(name=group_name)

    return group

def create_test_user(username='testuser', password='12345678'):
    user = AtlasUser.objects.create_user(username=username, password=password)

    return user

def create_test_source(title='testsource', url='http://localhost:8050/api/ows', source_type=Source.SOURCE_OWS):
    source = Source.objects.create(
        title=title,
        url=url,
        source_type=source_type
    )

    return source

def create_test_layer(title='testlayer', layer_name="testlayername"):
    layer = Layer.objects.create(
        title=title,
        layer_name=layer_name,
        layer_source=create_test_source()
    )

    return layer
