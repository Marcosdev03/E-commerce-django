# Rotas

## Rotas globais (`loja/urls.py`)

- `/admin/` -> admin Django
- `/perfil/` -> app `perfil`
- `/pedido/` -> app `pedido`
- `/endereco/` -> app `endereco`
- `/carrinho_de_compras/` -> app `carrinho_de_compras`
- `/` -> app `produto`

## Produto

Arquivo: `produto/urls.py`

- `GET /` -> lista de produtos (`produto:lista`)
- `GET /<slug>/` -> detalhe do produto (`produto:detalhe`)
- `GET /excluir/<slug>/` -> endpoint placeholder (`produto:excluir`)

Query params da lista:

- `?categoria=<slug_da_categoria>`
- `?q=<termo_de_busca>`

## Perfil

Arquivo: `perfil/urls.py`

- `GET|POST /perfil/` -> cadastro (`perfil:perfil`)
- `GET|POST /perfil/atualizar/` -> atualizacao (`perfil:atualizar`)
- `GET|POST /perfil/login/` -> login (`perfil:login`)
- `GET /perfil/logout/` -> logout (`perfil:logout`)

## Endereco

Arquivo: `endereco/urls.py`

- `GET|POST /endereco/` -> novo endereco (`endereco:inicio`)
- `GET|POST /endereco/novo/` -> novo endereco (`endereco:novo`)
- `GET|POST /endereco/editar/<pk>/` -> edicao (`endereco:editar`)
- `GET|POST /endereco/excluir/<pk>/` -> exclusao (`endereco:excluir`)

## Carrinho

Arquivo: `carrinho_de_compras/urls.py`

- `GET /carrinho_de_compras/` -> carrinho (`carrinho_de_compras:carrinho`)
- `GET /carrinho_de_compras/adicionaraocarrinho/?vid=<variacao_id>` -> adiciona item
- `GET /carrinho_de_compras/removerdocarrinho/?vid=<variacao_id>` -> remove item
- `GET /carrinho_de_compras/atualizar/` -> endpoint placeholder

## Pedido

Arquivo: `pedido/urls.py`

- `GET /pedido/` -> resumo antes de fechar (`pedido:pagar`)
- `GET /pedido/fecharpedido/<pedido_id>/` -> avanca status (`pedido:fechar-pedido`)
- `GET /pedido/detalhe/<pedido_id>/` -> detalhe do pedido (`pedido:detalhe`)
