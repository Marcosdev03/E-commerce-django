from decimal import Decimal, InvalidOperation


def formata_preco(valor):
    try:
        numero = Decimal(str(valor))
    except (InvalidOperation, ValueError, TypeError):
        return valor  # se não for número, retorna como está

    valor_formatado = f'{numero:,.2f}'
    valor_formatado = valor_formatado.replace(',', 'X').replace('.', ',').replace('X', '.')
    return f'R$ {valor_formatado}'