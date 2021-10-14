from django.conf import settings
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from user_management.models import AtlasUser


class AtlasOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = self.UserModel.objects.create_user(claims.get(settings.OIDC_USERNAME_CLAIM), claims.get('email'))
        user.first_name = claims.get('name')
        user.save()

        if settings.OIDC_ACTIVATE_ON_CREATE != 'True':
            user.is_active = False
            user.save()

    def update_user(self, user, claims):
        user.first_name = claims.get('name')
        user.email = claims.get('email')
        user.save()

        return user

    def filter_users_by_claims(self, claims):
        return AtlasUser.objects.filter(username__iexact=claims.get(settings.OIDC_USERNAME_CLAIM))
