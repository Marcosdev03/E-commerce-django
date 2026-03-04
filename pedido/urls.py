from . import views
from django.urls import path


app_name = 'pedido'


urlpatterns = [
    path('', views.Pagar.as_view(), name='pagar'),
    path('fecharpedido/', views.FecharPedido.as_view(), name='fechar-pedido'),
    path('detalhe/', views.Detalhe.as_view(), name='detalhe'),
]
