from rest_framework import routers

from authz import viewsets as authz_viewsets
from . import viewsets

api_router = routers.DefaultRouter()
api_router.register(r'maps', viewsets.MapViewSet, basename='maps')
api_router.register(r'sources', viewsets.SourceViewSet, basename='sources')
api_router.register(r'layers', viewsets.LayerViewSet, basename='layers')
api_router.register(r'drawings', viewsets.DrawingViewSet, basename='drawings')
api_router.register(
    r'categories', viewsets.CategoriesViewSet, basename='categories')
api_router.register(r'users', viewsets.UsersViewSet, basename='users')
api_router.register(r'groups', viewsets.GroupsViewSet, basename='groups')
api_router.register(
    r'authorize', authz_viewsets.AuthorizeViewSet, basename='autorize')

api_router.register(r'authorizations', authz_viewsets.AuthorizationViewSet, basename='authorizations')
api_router.register(r'configurations', viewsets.ConfigurationViewSet, basename='configurations')

api_router.register(r"metadatasets/topic-categories", viewsets.TopicCategoryViewSet, basename="topic-categories")
api_router.register(r"metadatasets/role-types", viewsets.RoleTypeViewSet, basename="role-types")
api_router.register(r"metadatasets/update-method-types", viewsets.UpdateMethodTypeViewSet,
                    basename="update-method-types")
api_router.register(r"metadatasets/authorization-level-types", viewsets.AuthorizationLevelTypeViewSet,
                    basename="authorization-level-types")
api_router.register(r"metadatasets/status-types", viewsets.StatusTypeViewSet, basename="status-types")
api_router.register(r"metadatasets/access-constraints-types", viewsets.AccessConstraintsTypeViewSet,
                    basename="access-constraints-types")
api_router.register(r"metadatasets/other-constraints-types", viewsets.OtherConstraintsTypeViewSet,
                    basename="other-constraints-types")

api_router.register(
    r'metadatasets', viewsets.MetadatasetViewSet, basename='metadatasets'
)
api_router.register(
    r'themes', viewsets.ThemeViewSet, basename='themes'
)
api_router.register(
    r'logs', viewsets.LogViewSet, basename='logs'
)

api_router.register(
    r'tables_old', viewsets.TableViewSet, basename='tables_old'
)
api_router.register(
    r'viewers', viewsets.ViewerViewSet, basename='viewers'
)