"""
Admin do produto
"""
from django.contrib import admin
from . import models


class VariacaoInline(admin.TabularInline):
    """
    Classe para exibir as variações do produto na página de administração do produto.
    """
    model = models.Variacao
    extra = 1


class ProdutoAdmin(admin.ModelAdmin):
    """
    Classe para exibir o produto na página de administração do produto.
    """
    inlines = [
        VariacaoInline
    ]


admin.site.register(models.Produto, ProdutoAdmin)
admin.site.register(models.Variacao)
