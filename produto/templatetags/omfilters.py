from django.template import Library
from utils.urls import formata_preco as formata_preco_utils

register = Library()

@register.filter
def formata_preco(valor):
    return formata_preco_utils(valor)


@register.filter(name='formatar_preco')
def formatar_preco(valor):
    return formata_preco_utils(valor)