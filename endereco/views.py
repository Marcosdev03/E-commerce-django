from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView


class NovoEndereco(View):
    """
    URL: /endereco/novo/
    """

    def get(self, *args, **kwargs):
        return HttpResponse('Formulário para criar um novo endereço')


class EditarEndereco(View):
    """
    URL: /endereco/editarendereco/<int:endereco_id>/
    """

    def get(self, *args, **kwargs):
        return HttpResponse('Formulário para editar um endereço existente')


class ExcluirEndereco(View):
    """
    URL: /endereco/excluir/<int:endereco_id>/
    """

    def get(self, *args, **kwargs):
        return HttpResponse('Confirmação para excluir um endereço existente')
