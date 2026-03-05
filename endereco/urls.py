from . import views
from django.urls import path


app_name = 'endereco'


urlpatterns = [
    path('novo/', views.NovoEndereco.as_view(), name='novo'),
    path('editar/<int:pk>/',
         views.EditarEndereco.as_view(), name='editar'),
    path('excluir/<int:pk>/',
         views.ExcluirEndereco.as_view(), name='excluir'),
]
