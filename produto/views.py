from . import models
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic import DetailView


class ListaProdutos(ListView):
    """
    URL: /produtos/
    """
    model = models.Produto
    template_name = "produto/produto_lista.html"
    context_object_name = "produtos"
    paginate_by = 10


class DetalheProduto(DetailView):
    """
    URL: /produtos/detalhe/<slug:slug>/
    """
    model = models.Produto
    template_name = "produto/detalhes.html"
    context_object_name = "produto"
    slug_url_kwarg = "slug"
    


class ExcluirProduto(View):
    """
    URL: /produtos/excluir/<int:produto_id>/
    """

    def get(self, *args, **kwargs):
        return HttpResponse("GET: Excluir produto")
