from django.template import Library
from utils.urls import formata_preco

register = Library()

@register.filter
def formatar_preco(val):
    return formata_preco(val)