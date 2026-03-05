from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView


class CriaPerfil(View):
    """
    URL: /perfil/
    """

    def get(self, *args, **kwargs):
        return HttpResponse("GET: Criar perfil")


class Atualizar(View):
    """
    URL: /perfil/atualizar/
    """

    def get(self, *args, **kwargs):
        return HttpResponse("GET: Atualizar perfil")
    pass


class Login(View):
    """
    URL: /perfil/login/
    """

    def get(self, *args, **kwargs):
        return HttpResponse("GET: Login")


class Logout(View):
    """
    URL: /perfil/logout/
    """

    def get(self, *args, **kwargs):
        return HttpResponse("GET: Logout")
