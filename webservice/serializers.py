from rest_framework import serializers

from user_management.models import AtlasUser
from .models import Map, Layer


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ['id', 'title', 'slug', 'features', 'settings', 'layers']


class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layer
        fields = ['id', 'title']


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    def get_groups(self, obj):
        return [group.name for group in obj.atlas_groups.all()]

    class Meta:
        model = AtlasUser
        fields = ['id', 'username', 'name', 'email', 'groups']
