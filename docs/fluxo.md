# Fluxo de Negocio

## 1. Catalogo

1. Usuario acessa `/`.
2. Pode filtrar por categoria (`categoria`) e buscar por nome (`q`).
3. Abre o detalhe do produto pelo slug.

## 2. Carrinho

1. No detalhe, seleciona variacao (`vid`) e adiciona ao carrinho.
2. Carrinho e salvo na sessao (`request.session['carrinho']`).
3. O sistema valida estoque antes de incrementar quantidade.
4. Usuario pode remover item no carrinho.

Estrutura resumida por item na sessao:

- `produto_id`, `produto_nome`
- `variacao_id`, `variacao_nome`
- `preco_unitario`, `preco_unitario_promocional`
- `preco_quantitativo`, `preco_quantitativo_promocional`
- `quantidade`, `slug`, `imagem`

## 3. Conta e endereco

1. Usuario cria conta em `/perfil/`.
2. Faz login em `/perfil/login/`.
3. Em `/perfil/atualizar/`, atualiza dados e gerencia enderecos.

## 4. Pedido

1. Usuario acessa `/pedido/`.
2. Validacoes obrigatorias:
   - usuario autenticado
   - carrinho nao vazio
   - pelo menos um endereco cadastrado
3. Sistema cria pedido com status `C` (criado) quando necessario.
4. Ao fechar pedido (`/pedido/fecharpedido/<id>/`):
   - `C` -> `P` (enviado para processamento)
   - `P` -> `F` (finalizado)
5. Sistema limpa dados de sessao do pedido/carrinho quando aplicavel.

## 5. Interface

- Navbar exibe categorias dinamicas e quantidade do carrinho.
- Mensagens de feedback usam `django.contrib.messages`.
- Tela de perfil mostra historico de pedidos e atalhos de acao.
