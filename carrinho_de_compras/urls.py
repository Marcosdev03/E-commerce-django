from django.urls import path
from . import views


app_name = 'carrinho_de_compras'

urlpatterns = [
    path('', views.Carrinho.as_view(), name='carrinho'),
    path('adicionar/<int:produto_id>/',
         views.AdicionarProduto.as_view(), name='adicionar'),
    path('removerdocarrinho/<int:produto_id>/',
         views.RemoverProdutoDoCarrinho.as_view(), name='remover'),
    path('atualizar/<int:produto_id>/',
         views.AtualizarProduto.as_view(), name='atualizar'),
]
