from . import views
from django.urls import path

app_name = 'perfil'

urlpatterns = [
    path('', views.CriaPerfil.as_view(), name='perfil'),
    path('atualizar/', views.Atualizar.as_view(), name='atualizar'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]
