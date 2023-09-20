from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import AtlasUser, AtlasGroup


class AtlasUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'name',
                    'is_staff', 'is_superuser', 'is_active')
    readonly_fields = ('external_id',)
    filter_horizontal = ('atlas_groups', )

    fieldsets = (
        (None, {'fields': ('username', 'external_id', 'password')}),
        (_('Personal info'), {
         'fields': ('name', 'email')}),
        (_('Permissions'), {
         'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Groups'), {'fields': ('atlas_groups',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


class MembershipInline(admin.TabularInline):
    model = AtlasUser.atlas_groups.through
    extra = 1


class AtlasGroupAdmin(admin.ModelAdmin):
    inlines = (MembershipInline,)


admin.site.register(AtlasUser, AtlasUserAdmin)

admin.site.unregister(Group)  # Unregister Django default groups
admin.site.register(AtlasGroup, AtlasGroupAdmin)
