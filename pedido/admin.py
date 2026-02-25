from django.contrib import admin
from . import models


class ItemPedidoInline(admin.TabularInline):
    """
    Classe para exibir os itens do pedido na página de administração do pedido.
    """
    model = models.ItemPedido
    extra = 1


class PedidoAdmin(admin.ModelAdmin):
    """
    Classe para exibir o pedido na página de administração do pedido.
    """
    inlines = [
        ItemPedidoInline
    ]


"""
Admin do pedido
"""
admin.site.register(models.Pedido, PedidoAdmin)
admin.site.register(models.ItemPedido)
