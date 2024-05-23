from django.contrib import admin
from .models import Apostila, ViewApostila


@admin.register(Apostila)
class ApostilasAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'titulo',
        'arquivo',
    ]


@admin.register(ViewApostila)
class ViewApostilaAdmin(admin.ModelAdmin):
    list_display = [
        'ip',
        'apostila',
    ]
