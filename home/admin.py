from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.translation import gettext_lazy as _

from home.models import CustomUser

admin.site.site_header = "Agrowise Administration"
admin.site.site_title = "Agrowise"
admin.site.index_title = "Agrowise"


@admin.register(CustomUser)
class UserAdmin(DefaultUserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {"fields": ("password",)}),
        (_("Extra ID"), {"fields": ("uid",)}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    # "username",
                    "email",
                    "mobile_no",
                    "gender",
                    "date_of_birth",
                    "profile_pic",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "date_of_birth",
                    "email",
                    "mobile_no",
                    "gender",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = [
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "date_joined",
        "last_login",
        "is_superuser",
        "is_staff",
    ]
    ordering = (
        "first_name",
        "last_name",
    )
    list_display_link = "name"
    list_display_links = ["first_name", "email"]
    list_filter = ["date_joined", "gender"]
    readonly_fields = ["uid"]
    search_fields = ["first_name", "last_name", "email", "mobile_no"]
