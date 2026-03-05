from django.views import View
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView


class Pagar(View):
    """
    URL: /pedido/
    """

    def get(self, *args, **kwargs):
        return HttpResponse('Formulário para pagamento do pedido')


class FecharPedido(View):
    """
    URL: /pedido/fecharpedido/<int:pedido_id>/
    """

    def get(self, *args, **kwargs):
        return HttpResponse('Confirmação para fechar o pedido')


class Detalhe(View):
    """
    URL: /pedido/detalhe/<int:pedido_id>/
    """

    def get(self, *args, **kwargs):
        return HttpResponse('Detalhes do pedido')
