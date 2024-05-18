from django.contrib import auth
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')

    elif request.method == 'POST':
        username = request.POST.get('username').lower()
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(
                request,
                constants.ERROR,
                'Senha e confirmar senha nao coincidem.'
            )

            return redirect('/usuarios/cadastro')

        user = User.objects.filter(
            username=username
        )

        if user.exists():
            messages.add_message(
                request,
                constants.ERROR,
                'Usuario ja existe.'
            )

            return redirect('/usuarios/cadastro')

        try:
            user = User.objects.create_user(
                username=username,
                password=senha
            )

            return redirect('/usuarios/logar')
        except:  # noqa
            messages.add_message(
                request,
                constants.ERROR,
                'Erro interno do servidor.'
            )

            return redirect('usuarios/cadastro')


def logar(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

    user = authenticate(request, username=username, password=senha)

    if user:
        auth.login(request, user)
        messages.add_message(
            request,
            constants.SUCCESS,
            f'Usuario {user} logado com sucesso!'
        )

        return redirect('/flashcard/novo_flashcard/')

    messages.add_message(
        request,
        constants.ERROR,
        'Usuario ou senha incorretos.'
    )

    return redirect('/usuarios/logar')


def logout(request):
    auth.logout(request)
    messages.add_message(
        request,
        constants.SUCCESS,
        'Usuario deslogado com sucesso!'
    )

    return redirect('/usuarios/logar')
