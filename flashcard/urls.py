from django.urls import path
from . import views

app_name = 'flashcard'

urlpatterns = [
    path(
        'novo_flashcard/',
        views.novo_flashcard,
        name='novo_flashcard'
    ),
    path(
        'deletar_flashcard/<int:id>/',
        views.deletar_flashcard,
        name='deletar_flashcard'
    ),
    path(
        'iniciar_desafio/',
        views.iniciar_desafio,
        name='iniciar_desafio'
    ),
    path(
        'listar_desafios/',
        views.listar_desafios,
        name='listar_desafios'
    ),
    path(
        'desafio/<int:id>/',
        views.desafio,
        name='desafio'
    ),
    path(
        'responder_flashcard/<int:id>/',
        views.responder_flashcard,
        name='responder_flashcard'
    ),
]
