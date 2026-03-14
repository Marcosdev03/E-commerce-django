from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from carrinho_de_compras.views import _obter_preco_total_item
from endereco.models import Endereco
from perfil.models import Perfil

from .models import ItemPedido, Pedido


def _criar_pedido_a_partir_do_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    if not carrinho:
        return None

    total = sum(_obter_preco_total_item(item) for item in carrinho.values())
    pedido = Pedido.objects.create(
        usuario=request.user,
        total=total,
        status='C',
    )

    for item in carrinho.values():
        ItemPedido.objects.create(
            pedido=pedido,
            produto=item.get('produto_nome', ''),
            produto_id=item.get('produto_id', 0),
            variacao=item.get('variacao_nome', ''),
            variacao_id=item.get('variacao_id'),
            preco=item.get('preco_unitario', 0),
            preco_promocional=item.get('preco_unitario_promocional'),
            quantidade=item.get('quantidade', 1),
            imagem=item.get('imagem', ''),
        )

    return pedido


class Pagar(LoginRequiredMixin, View):
    """
    URL: /pedido/
    """

    def get(self, *args, **kwargs):
        perfil, _ = Perfil.objects.get_or_create(usuario=self.request.user)
        endereco = perfil.enderecos.first()
        carrinho = self.request.session.get('carrinho', {})

        if not carrinho:
            messages.error(self.request, 'Seu carrinho está vazio.')
            return redirect('carrinho_de_compras:carrinho')

        if not endereco:
            messages.error(self.request, 'Cadastre um endereço antes de fechar o pedido.')
            return redirect('endereco:novo')

        pedido_id = self.request.session.get('pedido_id')
        pedido = None
        if pedido_id:
            pedido = Pedido.objects.filter(
                id=pedido_id,
                usuario=self.request.user,
                status='C',
            ).first()

        if not pedido:
            pedido = _criar_pedido_a_partir_do_carrinho(self.request)
            self.request.session['pedido_id'] = pedido.id
            self.request.session.save()

        contexto = {
            'pedido': pedido,
            'itens': pedido.itempedido_set.all(),
            'endereco': endereco,
        }
        return render(self.request, 'pedido/pagar.html', contexto)


class FecharPedido(LoginRequiredMixin, View):
    """
    URL: /pedido/fecharpedido/<int:pedido_id>/
    """

    def get(self, *args, **kwargs):
        pedido_id = kwargs.get('pedido_id')
        pedido = get_object_or_404(Pedido, id=pedido_id, usuario=self.request.user)

        if pedido.status == 'C':
            pedido.status = 'P'
            pedido.save()

            if self.request.session.get('pedido_id') == pedido.id:
                del self.request.session['pedido_id']

            if self.request.session.get('carrinho'):
                del self.request.session['carrinho']

            self.request.session.save()
            messages.success(self.request, 'Pedido enviado para processamento.')
            return redirect('pedido:detalhe', pedido_id=pedido.id)

        if pedido.status == 'P':
            pedido.status = 'F'
            pedido.save()
            messages.success(self.request, 'Pedido finalizado com sucesso.')
            return redirect('pedido:detalhe', pedido_id=pedido.id)

        messages.info(self.request, 'Esse pedido já foi processado.')
        return redirect('pedido:detalhe', pedido_id=pedido.id)


class Detalhe(LoginRequiredMixin, View):
    """
    URL: /pedido/detalhe/<int:pedido_id>/
    """

    def get(self, *args, **kwargs):
        pedido_id = kwargs.get('pedido_id')
        pedido = get_object_or_404(Pedido, id=pedido_id, usuario=self.request.user)
        itens = pedido.itempedido_set.all()
        endereco = Endereco.objects.filter(perfil__usuario=self.request.user).first()

        return render(
            self.request,
            'pedido/detalhe.html',
            {'pedido': pedido, 'itens': itens, 'endereco': endereco},
        )
