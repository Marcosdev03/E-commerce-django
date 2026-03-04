from . import views
from django.urls import path


app_name = 'endereco'


urlpatterns = [
    path('novo/', views.NovoEndereco.as_view(), name='novo'),
    path('editarendereco/<int:pk>/',
         views.EditarEndereco.as_view(), name='editarendereco'),
    path('excluirendereco/<int:pk>/',
         views.ExcluirEndereco.as_view(), name='excluirendereco'),
]
