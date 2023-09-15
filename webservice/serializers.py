from rest_framework import serializers

from .models import Drawing, Map, Source, Layer
from .authorization import can_request_access_layer


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ['id', 'title', 'slug', 'features', 'settings', 'layers']


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'title', 'slug', 'url', 'authenticate']


class LayerSerializer(serializers.ModelSerializer):
    can_access = serializers.SerializerMethodField('get_can_access')

    def get_can_access(self, obj):
        request = self.context['request']
        return can_request_access_layer(request, obj)

    class Meta:
        model = Layer
        fields = [
            'id',
            'title',
            'can_access',
            'slug',
            'layer_name'
        ]


class DrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drawing
        fields = ['id', 'features']
