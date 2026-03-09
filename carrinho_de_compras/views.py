from produto.models import Variacao
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, redirect, reverse, get_object_or_404

class Carrinho(View):
    """
    URL: /carrinho/
    """

    def get(self, *args, **kwargs):
        return HttpResponse('Visualização do carrinho de compras')


class AdicionarAoCarrinho(View):
    """
    URL: /carrinho/adicionar/<int:produto_id>/
    """

    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER', reverse(
            'produto:lista')) 
        
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(self.request, 'Produto não encontrado')
            return redirect(http_referer)
        
        variacao = get_object_or_404(Variacao, id=variacao_id)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            # TODO: Variação existe no carrinho.
            pass
        else:
            # TODO: Variação não existe no carrinho.
            pass

        return HttpResponse(f'Adicionar o produto {variacao} ao carrinho de compras')


class RemoverProdutoDoCarrinho(View):
    """
    URL: /carrinho/removerdocarrinho/<int:produto_id>/
    """

    def get(self, *args, **kwargs):
        return HttpResponse('Remover um produto do carrinho de compras')


class AtualizarProdutoDoCarrinho(View):
    """ 
    URL: /carrinho/atualizar/<int:produto_id>/
    """

    def get(self, *args, **kwargs):
        return HttpResponse('Atualizar a quantidade de um produto no carrinho de compras')
