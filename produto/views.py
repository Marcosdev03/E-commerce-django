from . import models
from django.views import View
from urllib.parse import urlencode
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

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-id')

        categoria_slug = self.request.GET.get('categoria', '').strip()
        termo_busca = self.request.GET.get('q', '').strip()

        if categoria_slug:
            queryset = queryset.filter(categoria__slug=categoria_slug)

        if termo_busca:
            queryset = queryset.filter(nome__icontains=termo_busca)

        return queryset

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        categoria = self.request.GET.get('categoria', '').strip()
        busca = self.request.GET.get('q', '').strip()
        contexto['categoria_selecionada'] = categoria
        contexto['busca'] = busca

        query_dict = {}
        if categoria:
            query_dict['categoria'] = categoria
        if busca:
            query_dict['q'] = busca
        contexto['extra_query'] = urlencode(query_dict)
        return contexto


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
