from django.contrib import admin

from .models import Cinema


class CinemaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "city",
        "address",
        "capacity",
        "is_disabled",
        "created_at",
    )
    list_filter = ("is_disabled", "city", "created_at")
    search_fields = ("name", "city", "address")
    ordering = ("name", "city")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)


admin.site.register(Cinema, CinemaAdmin)
