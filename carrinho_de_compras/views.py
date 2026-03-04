from django.views import View
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView


class Carrinho(View):
    """
    URL: /carrinho/
    """

    def get(self, *args, **kwargs):
        return HttpResponse('Visualização do carrinho de compras')


class AdicionarProduto(View):
    """
    URL: /carrinho/adicionar/<int:produto_id>/
    """

    def get(self, *args, **kwargs):
        return HttpResponse('Adicionar um produto ao carrinho de compras')


class RemoverProdutoDoCarrinho(View):
    """
    URL: /carrinho/removerdocarrinho/<int:produto_id>/
    """

    def get(self, *args, **kwargs):
        return HttpResponse('Remover um produto do carrinho de compras')


class AtualizarProduto(View):
    """ 
    URL: /carrinho/atualizar/<int:produto_id>/
    """

    def get(self, *args, **kwargs):
        return HttpResponse('Atualizar a quantidade de um produto no carrinho de compras')
