from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView


class ListaProdutos(View):
    """
    URL: /produtos/
    """

    def get(self, *args, **kwargs):
        return HttpResponse("GET: Lista de produtos")


class DetalheProduto(View):
    """
    URL: /produtos/detalhe/<int:produto_id>/
    """

    def get(self, *args, **kwargs):
        return HttpResponse("GET: Detalhe do produto")


class ExcluirProduto(View):
    """
    URL: /produtos/excluir/<int:produto_id>/
    """

    def get(self, *args, **kwargs):
        return HttpResponse("GET: Excluir produto")
