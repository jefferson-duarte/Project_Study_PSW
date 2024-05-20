from django.contrib import admin
from .models import Categoria, Flashcard, FlashcardDesafio, Desafio


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


@admin.register(FlashcardDesafio)
class FlashcardDesafioAdmin(admin.ModelAdmin):
    list_display = [
        'flashcard',
        'respondido',
        'acertou',
    ]


@admin.register(Desafio)
class DesafioAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'titulo',
        'quantidade_perguntas',
        'dificuldade',
    ]
