from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from perfil.models import Perfil

from .forms import EnderecoForm
from .models import Endereco


class NovoEndereco(LoginRequiredMixin, View):
    """
    URL: /endereco/novo/
    """

    def get(self, *args, **kwargs):
        return render(self.request, 'endereco/form.html', {'form': EnderecoForm()})

    def post(self, *args, **kwargs):
        form = EnderecoForm(self.request.POST)

        if not form.is_valid():
            messages.error(self.request, 'Existem erros no cadastro de endereço.')
            return render(self.request, 'endereco/form.html', {'form': form})

        perfil, _ = Perfil.objects.get_or_create(usuario=self.request.user)
        endereco = form.save(commit=False)
        endereco.perfil = perfil
        endereco.save()

        messages.success(self.request, 'Endereço cadastrado com sucesso.')
        return redirect('perfil:atualizar')


class EditarEndereco(LoginRequiredMixin, View):
    """
    URL: /endereco/editarendereco/<int:endereco_id>/
    """

    def get(self, *args, **kwargs):
        endereco = get_object_or_404(
            Endereco,
            pk=kwargs.get('pk'),
            perfil__usuario=self.request.user,
        )
        form = EnderecoForm(instance=endereco)
        return render(self.request, 'endereco/form.html', {'form': form, 'endereco': endereco})

    def post(self, *args, **kwargs):
        endereco = get_object_or_404(
            Endereco,
            pk=kwargs.get('pk'),
            perfil__usuario=self.request.user,
        )
        form = EnderecoForm(self.request.POST, instance=endereco)

        if not form.is_valid():
            messages.error(self.request, 'Existem erros na atualização do endereço.')
            return render(
                self.request,
                'endereco/form.html',
                {'form': form, 'endereco': endereco},
            )

        form.save()
        messages.success(self.request, 'Endereço atualizado com sucesso.')
        return redirect('perfil:atualizar')


class ExcluirEndereco(LoginRequiredMixin, View):
    """
    URL: /endereco/excluir/<int:endereco_id>/
    """

    def get(self, *args, **kwargs):
        endereco = get_object_or_404(
            Endereco,
            pk=kwargs.get('pk'),
            perfil__usuario=self.request.user,
        )
        return render(self.request, 'endereco/excluir.html', {'endereco': endereco})

    def post(self, *args, **kwargs):
        endereco = get_object_or_404(
            Endereco,
            pk=kwargs.get('pk'),
            perfil__usuario=self.request.user,
        )
        endereco.delete()
        messages.success(self.request, 'Endereço removido com sucesso.')
        return redirect('perfil:atualizar')
