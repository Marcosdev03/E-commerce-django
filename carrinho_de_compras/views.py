from pprint import pprint
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
        return render(self.request, 'carrinho_de_compras/carrinho.html')


class AdicionarAoCarrinho(View):
    """
    URL: /carrinho/adicionar/<int:produto_id>/
    """

    def get(self, *args, **kwargs):

        # TODO: REMOVER LINHAS ABAIXO
        #if self.request.session.get('carrinho'):
            #del self.request.session['carrinho']
            #self.request.session.save()

        http_referer = self.request.META.get('HTTP_REFERER', reverse(
            'produto:lista')) 
        
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(self.request, 'Produto não encontrado')
            return redirect(http_referer)
        
        variacao = get_object_or_404(Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug    
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''


        if variacao.estoque < 1:
            messages.error(self.request, 'Produto sem estoque')
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.error(
                    self.request, 
                    'Não temos estoque suficiente para ' \
                    'adicionar mais desse produto no seu carrinho'
                    
                )
                quantidade_carrinho = variacao_estoque

                return redirect(http_referer)

            carrinho[variacao_id]['quantidade'] = quantidade_carrinho

            carrinho[variacao_id]['preco_quantitativo'] = (
                preco_unitario * quantidade_carrinho)
            
            carrinho[variacao_id]['preco_quantativo_promocional'] = (
                preco_unitario_promocional * quantidade_carrinho)
        else:
            carrinho[variacao_id] = {
                    'produto_id': produto_id,
                    'produto_nome': produto_nome,
                    'variacao_nome': variacao_nome,
                    'variacao_id': variacao_id,
                    'preco_unitario': preco_unitario,
                    'preco_unitario_promocional': preco_unitario_promocional,
                    'preco_quantitativo': preco_unitario,
                    'preco_quantitativo_promocional': preco_unitario_promocional,
                    'quantidade': quantidade,
                    'slug': slug,
                    'imagem': imagem
            }

        self.request.session.save()
        
        messages.success(
            self.request, f'{produto.nome} adicionado ao carrinho de compras')
        return redirect(http_referer)


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
