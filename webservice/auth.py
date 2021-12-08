from django.conf import settings
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from user_management.models import AtlasUser


class AtlasOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        user = self.UserModel.objects.create_user(claims.get(settings.OIDC_USERNAME_CLAIM), claims.get('email'))

        if claims.get('name'):
            user.first_name = claims.get('name')
        elif claims.get('sub'):
            user.first_name = claims.get('sub')

        user.save()

        print(claims)
        print(self.request.session.get('oidc_access_token'))

        if settings.OIDC_ACTIVATE_ON_CREATE != 'True':
            user.is_active = False
            user.save()

    def update_user(self, user, claims):
        if claims.get('name'):
            user.first_name = claims.get('name')
        elif claims.get('sub'):
            user.first_name = claims.get('sub')

        if claims.get('email'):
            user.email = claims.get('email')

        user.save()

        return user

    def filter_users_by_claims(self, claims):
        return AtlasUser.objects.filter(username__iexact=claims.get(settings.OIDC_USERNAME_CLAIM))

    def verify_claims(self, claims):
        print('Verifying claims')

        print(claims)
        print(self.request.session.get('oidc_access_token'))

        return True
