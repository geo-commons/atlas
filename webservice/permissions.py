from rest_framework.permissions import IsAdminUser, SAFE_METHODS


class IsAtlasAdmin(IsAdminUser):
    def has_permission(self, request, view) -> bool:
        user = request.user
        return bool(user and user.is_authenticated and user.is_staff and user.is_superuser)


class IsAdminOrReadOnly(IsAdminUser):
    def has_permission(self, request, view) -> bool:
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        return bool(user and user.is_staff and user.is_superuser)
