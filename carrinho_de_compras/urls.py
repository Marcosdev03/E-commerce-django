from django.urls import path
from . import views


app_name = 'carrinho_de_compras'

urlpatterns = [
    path('', views.Carrinho.as_view(), name='carrinho'),
    path('adicionaraocarrinho/',
         views.AdicionarProduto.as_view(), name='adicionaraocarrinho'),
    path('removerdocarrinho/',
         views.RemoverProdutoDoCarrinho.as_view(), name='remover'),
    path('atualizar/',
         views.AtualizarProduto.as_view(), name='atualizar'),
]
