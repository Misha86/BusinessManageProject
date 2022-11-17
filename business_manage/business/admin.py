"""Configuration for admin."""

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import (UserAdmin as BaseUserAdmin,
                                       GroupAdmin as BaseGroupAdmin)
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


admin.site.unregister(Group)


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Class for specifing CustomUser fields in admin."""
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ("email", "first_name", "last_name", "position", "id")
    list_filter = ("groups", "position")
    fieldsets = (
        (None, {"fields": ("email", "password", "groups")}),
        ("Personal info", {"fields": ("first_name", "last_name", "patronymic", "position", "bio", "avatar")}),
        ("Permissions", {"fields": ("is_active", )}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "patronymic",
                       "position", "groups", "avatar", "password1", "password2"),
        }),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


class CustomUserInline(admin.TabularInline):
    """Class allows to add CustomUser in Group admin page."""
    model = CustomUser.groups.through
    extra = 1


@admin.register(Group)
class CustomGroupAdmin(BaseGroupAdmin):
    """Extends BaseGroupAdmin class adding CustomUserInline class."""
    inlines = [
        CustomUserInline,
    ]
