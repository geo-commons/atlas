from rest_framework import serializers

from .models import AtlasTheme

class AtlasThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtlasTheme
        fields = ['title', 'slug']
