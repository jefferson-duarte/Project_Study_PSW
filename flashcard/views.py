from django.http import Http404
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
        titulo = request.POST.get('titulo').strip()
        categorias = request.POST.getlist('categoria')
        dificuldade = request.POST.get('dificuldade')
        qtd_perguntas = request.POST.get('qtd_perguntas')

        if titulo == '':
            messages.add_message(
                request,
                constants.ERROR,
                'Favor, adicionar um título.'
            )
            return redirect(reverse('flashcard:iniciar_desafio'))

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

        url = reverse('flashcard:listar_desafios')

        return redirect(url)


def listar_desafios(request):
    if request.method == 'GET':
        desafios = Desafio.objects.filter(
            user=request.user
        )
        context = {
            'desafios': desafios,
        }

        return render(request, 'listar_desafio.html', context)


def desafio(request, id):
    desafio = Desafio.objects.get(id=id)

    if not desafio.user == request.user:
        raise Http404()

    if request.method == 'GET':
        acertos = desafio.flashcards.filter(
            respondido=True
        ).filter(
            acertou=True
        ).count()

        erros = desafio.flashcards.filter(
            respondido=True
        ).filter(
            acertou=False
        ).count()

        faltantes = desafio.flashcards.filter(
            respondido=False
        ).count()

        context = {
            'desafio': desafio,
            'acertos': acertos,
            'erros': erros,
            'faltantes': faltantes,
        }

    return render(request, 'desafio.html', context)


def responder_flashcard(request, id):
    flashcard_desafio = FlashcardDesafio.objects.get(id=id)
    acertou = request.GET.get('acertou')
    desafio_id = request.GET.get('desafio_id')

    if not flashcard_desafio.flashcard.user == request.user:
        messages.add_message(
            request,
            constants.ERROR,
            'Erro ao buscar flash card.'
        )

        return redirect(reverse('flashcard:desafio'))

    flashcard_desafio.respondido = True

    flashcard_desafio.acertou = True if acertou == '1' else False
    flashcard_desafio.save()

    url = reverse('flashcard:desafio', args=[desafio_id])

    return redirect(url)
