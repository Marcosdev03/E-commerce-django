from . import models
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView


class ListaProdutos(ListView):
    """
    URL: /produtos/
    """
    model = models.Produto
    template_name = "produto/produto_lista.html"
    context_object_name = "produtos"
    paginate_by = 10


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
