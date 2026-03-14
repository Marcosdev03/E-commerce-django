from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from pedido.models import Pedido

from .forms import LoginForm, PerfilForm, UserForm, UserUpdateForm
from .models import Perfil


class CriaPerfil(View):
    """
    URL: /perfil/
    """

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('perfil:atualizar')

        contexto = {
            'user_form': UserForm(),
            'perfil_form': PerfilForm(),
        }
        return render(self.request, 'perfil/criar.html', contexto)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('perfil:atualizar')

        user_form = UserForm(self.request.POST)
        perfil_form = PerfilForm(self.request.POST)

        if not user_form.is_valid() or not perfil_form.is_valid():
            messages.error(self.request, 'Existem erros no formulário de cadastro.')
            return render(
                self.request,
                'perfil/criar.html',
                {'user_form': user_form, 'perfil_form': perfil_form},
            )

        usuario = user_form.save(commit=False)
        usuario.set_password(user_form.cleaned_data['password'])
        usuario.save()

        perfil = perfil_form.save(commit=False)
        perfil.usuario = usuario
        perfil.save()

        messages.success(self.request, 'Conta criada com sucesso. Faça login para continuar.')
        return redirect('perfil:login')


class Atualizar(LoginRequiredMixin, View):
    """
    URL: /perfil/atualizar/
    """

    def get(self, *args, **kwargs):
        perfil, _ = Perfil.objects.get_or_create(usuario=self.request.user)
        pedidos = Pedido.objects.filter(usuario=self.request.user).order_by('-id')
        contexto = {
            'user_form': UserUpdateForm(instance=self.request.user),
            'perfil_form': PerfilForm(instance=perfil),
            'enderecos': perfil.enderecos.all(),
            'pedidos': pedidos,
        }
        return render(self.request, 'perfil/atualizar.html', contexto)

    def post(self, *args, **kwargs):
        perfil, _ = Perfil.objects.get_or_create(usuario=self.request.user)
        user_form = UserUpdateForm(self.request.POST, instance=self.request.user)
        perfil_form = PerfilForm(self.request.POST, instance=perfil)

        if not user_form.is_valid() or not perfil_form.is_valid():
            pedidos = Pedido.objects.filter(usuario=self.request.user).order_by('-id')
            messages.error(self.request, 'Existem erros no formulário de atualização.')
            return render(
                self.request,
                'perfil/atualizar.html',
                {
                    'user_form': user_form,
                    'perfil_form': perfil_form,
                    'enderecos': perfil.enderecos.all(),
                    'pedidos': pedidos,
                },
            )

        user_form.save()
        perfil_form.save()
        messages.success(self.request, 'Perfil atualizado com sucesso.')
        return redirect('perfil:atualizar')


class Login(View):
    """
    URL: /perfil/login/
    """

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('perfil:atualizar')

        return render(self.request, 'perfil/login.html', {'form': LoginForm()})

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('perfil:atualizar')

        form = LoginForm(self.request.POST)

        if not form.is_valid():
            messages.error(self.request, 'Dados de login inválidos.')
            return render(self.request, 'perfil/login.html', {'form': form})

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        usuario = authenticate(self.request, username=username, password=password)

        if not usuario:
            messages.error(self.request, 'Usuário ou senha inválidos.')
            return render(self.request, 'perfil/login.html', {'form': form})

        login(self.request, usuario)
        messages.success(self.request, f'Login realizado com sucesso, {usuario.username}.')
        return redirect('produto:lista')


class Logout(View):
    """
    URL: /perfil/logout/
    """

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
            messages.success(self.request, 'Você saiu da sua conta.')

        return redirect('produto:lista')
