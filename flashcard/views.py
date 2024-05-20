from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Categoria, Flashcard, Desafio, FlashcardDesafio
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

        categoria_filtrar = request.GET.get('categoria')
        dificuldade_filtrar = request.GET.get('dificuldade')

        if categoria_filtrar:
            flashcards = flashcards.filter(categoria__id=categoria_filtrar)

        if dificuldade_filtrar:
            flashcards = flashcards.filter(dificuldade=dificuldade_filtrar)

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


def deletar_flashcard(request, id):

    if request.method == 'GET':
        flashcard = Flashcard.objects.filter(
            user=request.user
        )

        flashcard = flashcard.get(id=id)
        name_flashcard = flashcard
        flashcard.delete()

        messages.add_message(
            request,
            constants.SUCCESS,
            f'Flashcard "{name_flashcard}" deletado com sucesso!'
        )

        return redirect(reverse('flashcard:novo_flashcard'))


def iniciar_desafio(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        context = {
            'categorias': categorias,
            'dificuldades': dificuldades,
        }

        return render(
            request,
            'iniciar_desafio.html',
            context,
        )

    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        categorias = request.POST.getlist('categoria')
        dificuldade = request.POST.get('dificuldade')
        qtd_perguntas = request.POST.get('qtd_perguntas')

        # if 0 > int(qtd_perguntas) == '':

        try:
            flashcards = Flashcard.objects.filter(
                user=request.user
            ).filter(
                dificuldade=dificuldade
            ).filter(
                categoria_id__in=categorias
            ).order_by('?')

            qtd_flashcards = flashcards.count()

            if qtd_flashcards < int(qtd_perguntas) or int(qtd_perguntas) == 0:
                messages.add_message(
                    request,
                    constants.ERROR,
                    f'Erro na quantidade de flash cards. Existem {
                        qtd_flashcards} flash cards disponíveis.'
                )

                return redirect(reverse('flashcard:iniciar_desafio'))

            flashcards = flashcards[:int(qtd_perguntas)]

        except ValueError:
            messages.add_message(
                request,
                constants.ERROR,
                'Erro, insira quantidades positivas.'
            )
            return redirect(reverse('flashcard:iniciar_desafio'))

        desafio = Desafio(
            user=request.user,
            titulo=titulo,
            quantidade_perguntas=qtd_perguntas,
            dificuldade=dificuldade
        )
        desafio.save()

        for categoria in categorias:
            desafio.categoria.add(categoria)

        for f in flashcards:
            flashcard_desafio = FlashcardDesafio(
                flashcard=f
            )
            flashcard_desafio.save()
            desafio.flashcards.add(flashcard_desafio)

        desafio.save()

        return HttpResponse('Teste')
