from django.contrib import admin
from . import models


class PerfilAdmin(admin.ModelAdmin):
    """
    Classe para exibir o perfil na página de administração do perfil.
    """
    list_display = ['usuario', 'telefone', 'idade']


admin.site.register(models.Perfil, PerfilAdmin)
