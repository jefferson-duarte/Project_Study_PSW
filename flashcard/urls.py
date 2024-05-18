from django.urls import path
from . import views

app_name = 'flashcard'

urlpatterns = [
    path('novo_flashcard/', views.novo_flashcard, name='novo_flashcard'),
]
