from pprint import pprint
from produto.models import Variacao
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, redirect, reverse, get_object_or_404


def _obter_preco_total_item(item):
    preco_promocional = item.get('preco_quantitativo_promocional')
    if preco_promocional is not None:
        return preco_promocional
    return item.get('preco_quantitativo', 0)


class Carrinho(View):
    def get(self, *args, **kwargs):
        carrinho = self.request.session.get('carrinho', {})

        total = sum(_obter_preco_total_item(item) for item in carrinho.values())
        
        contexto = {
            'carrinho': carrinho,
            'preco_quantitativo': total
        }
        
        return render(self.request, 'carrinho_de_compras/carrinho.html', contexto)


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

                

            carrinho[variacao_id]['quantidade'] = quantidade_carrinho

            carrinho[variacao_id]['preco_quantitativo'] = (
                preco_unitario * quantidade_carrinho)
            
            carrinho[variacao_id]['preco_quantitativo_promocional'] = (
                preco_unitario_promocional * quantidade_carrinho
                if preco_unitario_promocional is not None and preco_unitario_promocional > 0 else None
            )
        else:
            carrinho[variacao_id] = {
                    'produto_id': produto_id,
                    'produto_nome': produto_nome,
                    'variacao_nome': variacao_nome,
                    'variacao_id': variacao_id,
                    'preco_unitario': preco_unitario,
                    'preco_unitario_promocional': preco_unitario_promocional,
                    'preco_quantitativo': preco_unitario,
                    'preco_quantitativo_promocional': preco_unitario_promocional if preco_unitario_promocional is not None and preco_unitario_promocional > 0 else None,
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
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(self.request, 'Produto não encontrado no carrinho.')
            return redirect('carrinho_de_compras:carrinho')

        carrinho = self.request.session.get('carrinho', {})

        if variacao_id not in carrinho:
            messages.error(self.request, 'Produto não encontrado no carrinho.')
            return redirect('carrinho_de_compras:carrinho')

        produto_nome = carrinho[variacao_id].get('produto_nome', 'Produto')
        del carrinho[variacao_id]
        self.request.session.save()

        messages.success(
            self.request,
            f'{produto_nome} removido do carrinho de compras.'
        )
        return redirect('carrinho_de_compras:carrinho')


class AtualizarProdutoDoCarrinho(View):
    """ 
    URL: /carrinho/atualizar/<int:produto_id>/
    """

    def get(self, *args, **kwargs):
        return HttpResponse('Atualizar a quantidade de um produto no carrinho de compras')
