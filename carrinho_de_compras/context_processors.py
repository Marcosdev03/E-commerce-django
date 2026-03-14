def quantidade_total_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    quantidade_total = sum(
        item.get('quantidade', 0) for item in carrinho.values()
    )

    return {
        'quantidade_total_carrinho': quantidade_total,
    }