from django.contrib import admin

from .models import Movie


class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "genre", "duration", "is_disabled", "created_at")
    list_filter = ("is_disabled", "genre", "created_at")
    search_fields = ("title", "genre")
    ordering = ("title", "genre")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)


admin.site.register(Movie, MovieAdmin)
