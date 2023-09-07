from rest_framework import serializers

from .models import Drawing, Map, Source, Layer
from utils.tools import is_internal


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
        user = request.user

        if not obj.is_published:
            return False

        if obj.closed_dataset and is_internal(request) is not True:
            return False

        if obj.login_required and user.is_anonymous:
            return False

        layer_only_accessible_by_groups = obj.atlas_groups.exists()

        if user.is_anonymous and not layer_only_accessible_by_groups:
            return True

        if user.is_anonymous and layer_only_accessible_by_groups:
            return False

        if not user.is_anonymous and not layer_only_accessible_by_groups:
            return True

        user_groups = user.atlas_groups.all()
        user_has_access_to_layer_via_group = any(
            g for g in obj.atlas_groups.all() if g in user_groups
        )

        if not user.is_anonymous and user_has_access_to_layer_via_group:
            return True

        if not user.is_anonymous and not user_has_access_to_layer_via_group:
            return False

        return False

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
