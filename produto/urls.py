from django.urls import path
from . import views

app_name = 'produto'

urlpatterns = [
    path('', views.ListaProdutos.as_view(), name='lista'),
    path('<slug:slug>/', views.DetalheProduto.as_view(), name='detalhe'),
    path('excluir/<slug:slug>/', views.ExcluirProduto.as_view(), name='excluir'),
]
