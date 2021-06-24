from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from user_management.models import AtlasUser


class AtlasOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = self.UserModel.objects.create_user(claims.get('sub'), claims.get('email'))
        user.first_name = claims.get('name')
        user.save()

    def update_user(self, user, claims):
        user.first_name = claims.get('name')
        user.email = claims.get('email')
        user.save()

        return user

    def filter_users_by_claims(self, claims):
        return AtlasUser.objects.filter(username__iexact=claims.get('sub'))
