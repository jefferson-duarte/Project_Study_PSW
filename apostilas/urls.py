from django.urls import path
from . import views

app_name = 'apostilas'

urlpatterns = [
    path(
        'adicionar_apostilas/',
        views.adicionar_apostilas,
        name='adicionar_apostilas'
    )
]
