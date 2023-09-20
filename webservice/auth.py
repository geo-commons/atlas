from django.conf import settings
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from user_management.models import AtlasUser, AtlasGroup


class AtlasOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = self.UserModel.objects.create_user(claims.get(
            settings.OIDC_USERNAME_CLAIM), claims.get('email'))
        user.name = claims.get('name')
        user.external_id = claims.get('sub')
        user.save()

        if not settings.OIDC_ACTIVATE_ON_CREATE:
            user.is_active = False
            user.save()

        if settings.OIDC_SYNC_GROUPS:
            groups_from_claim = claims.get('groups', [])

            elegible_groups = AtlasGroup.objects.filter(
                external_id__in=groups_from_claim)

            for group in elegible_groups:
                user.atlas_groups.add(group)

        return user

    def update_user(self, user, claims):
        user.name = claims.get('name')
        user.email = claims.get('email')
        user.save()

        if settings.OIDC_SYNC_GROUPS:
            groups_from_claim = claims.get('groups', [])

            groups_to_add = AtlasGroup.objects.filter(
                external_id__in=groups_from_claim).exclude(atlas_users=user)

            groups_to_remove = AtlasGroup.objects.filter(
                atlas_users=user, external_id__isnull=False).exclude(external_id__in=groups_from_claim)

            for group in groups_to_add:
                user.atlas_groups.add(group)

            for group in groups_to_remove:
                user.atlas_groups.remove(group)

        return user

    def filter_users_by_claims(self, claims):
        return AtlasUser.objects.filter(username__iexact=claims.get(settings.OIDC_USERNAME_CLAIM))
