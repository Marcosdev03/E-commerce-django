def formata_preco(valor):
    try:
        numero = float(valor)
    except (ValueError, TypeError):
        return valor  # se não for número, retorna como está
    return f'R$ {numero:.2f}'.replace('.', ',')