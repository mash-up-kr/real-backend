from django.contrib import admin
from .models import Dream, Result


class ResultInline(admin.TabularInline):
    model = Result


@admin.register(Dream)
class DreamAdmin(admin.ModelAdmin):
    inlines = [ResultInline]


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    pass
