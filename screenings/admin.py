# Register your models here.
from django.contrib import admin

from .models import Screening, Seat


class ScreeningAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "movie",
        "cinema",
        "date",
        "price",
        "is_dubbed",
        "is_subtitled",
        "is_disabled",
        "created_at",
    )
    list_filter = (
        "is_dubbed",
        "is_subtitled",
        "is_disabled",
        "created_at",
        "movie",
        "cinema",
    )
    search_fields = ("movie__title", "cinema__name", "date")
    ordering = ("date", "movie")
    date_hierarchy = "date"
    readonly_fields = ("created_at",)

    def has_add_permission(self, request):
        return False


admin.site.register(Screening, ScreeningAdmin)


class SeatAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "screening",
        "booking",
        "number",
        "is_reserved",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_reserved", "created_at", "screening")
    search_fields = ("screening__movie__title", "number")
    ordering = ("screening", "number")
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Seat, SeatAdmin)
