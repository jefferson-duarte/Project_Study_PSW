from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Categoria, Flashcard
from django.http import HttpResponse
from django.contrib.messages import constants
from django.contrib import messages


def novo_flashcard(request):
    if not request.user.is_authenticated:
        return redirect(reverse('usuarios:login'))

    if request.method == 'GET':
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        flashcards = Flashcard.objects.filter(
            user=request.user
        )

        context = {
            'categorias': categorias,
            'dificuldades': dificuldades,
            'flashcards': flashcards,
        }

        return render(request, 'novo_flashcard.html', context)

    elif request.method == 'POST':
        pergunta = request.POST.get('pergunta')
        resposta = request.POST.get('resposta')
        categoria = request.POST.get('categoria')
        dificuldade = request.POST.get('dificuldade')

        if len(pergunta.strip()) == 0 or len(resposta.strip()) == 0:
            messages.add_message(
                request,
                constants.ERROR,
                'Preencha os campos de pergunta e resposta.'
            )

            return redirect(reverse('flashcard:novo_flashcard'))

        flashcard = Flashcard(
            user=request.user,
            pergunta=pergunta,
            resposta=resposta,
            categoria_id=categoria,
            dificuldade=dificuldade,
        )

        flashcard.save()
        messages.add_message(
            request,
            constants.SUCCESS,
            'Flashcard cadastrado com sucesso!'
        )

        return redirect(reverse('flashcard:novo_flashcard'))
