# Register your models here.
from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "username",
        "date_joined",
        "is_active",
    )
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_active", "date_joined")
    ordering = ("-date_joined",)


admin.site.register(User, UserAdmin)
