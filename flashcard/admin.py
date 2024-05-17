from django.contrib import admin
from .models import Categoria, Flashcard


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = [
        'nome'
    ]


@admin.register(Flashcard)
class FlashcardsAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'pergunta',
        'resposta',
        'categoria',
        'dificuldade',
    ]
