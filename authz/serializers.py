from rest_framework import serializers

from authz.models import Authorization


class AuthorizationSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        self.title = obj.resource
        return self.title

    class Meta:
        model = Authorization
        fields = ['id', 'title', 'source', 'ordering', 'resource', 'description', 'login_required', 'only_internal', 'audit_log', 'response_filter', 'atlas_groups']