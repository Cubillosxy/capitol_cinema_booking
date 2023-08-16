from django.contrib import admin  # noqa

from .models import Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "screening",
        "user",
        "is_cancelled",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_cancelled", "is_active", "created_at", "updated_at")
    search_fields = ["user__email"]
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Booking, BookingAdmin)
