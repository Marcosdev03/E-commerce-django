from django.contrib import admin
from . import models


class EnderecoAdmin(admin.ModelAdmin):
    """
    Classe para exibir o endereço na página de administração do endereço.
    """
    list_display = ['perfil', 'rua', 'numero', 'cidade', 'estado', 'cep']


admin.site.register(models.Endereco, EnderecoAdmin)
