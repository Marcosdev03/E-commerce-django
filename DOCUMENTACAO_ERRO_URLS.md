# Diagnostico das URLs do Projeto

Data: 09/03/2026

## O que estava errado

Havia um conflito de roteamento entre as URLs globais do projeto e as URLs do app `produto`.

Arquivos envolvidos:
- `loja/urls.py`
- `produto/urls.py`

Pontos criticos:
1. Em `loja/urls.py`, o include de `produto.urls` estava na raiz (`path('', include('produto.urls'))`) e aparecia antes de outras rotas importantes.
2. Em `produto/urls.py`, existia uma rota generica `path('<slug:slug>/', ...)`.
3. Como essa rota generica aceita qualquer segmento unico, ela podia capturar caminhos que deveriam ir para outros apps (exemplo: `perfil/`, `pedido/`, etc.).

## Consequencia pratica

Mesmo sem erro de sintaxe no `manage.py check`, o comportamento de navegacao poderia ficar incorreto.

Exemplo de risco:
- URL esperada: `/perfil/` (app `perfil`)
- URL possivelmente capturada: `/<slug>/` no app `produto`

Isso pode causar:
- pagina errada sendo exibida
- 404 inesperado dentro da view de produto
- dificuldade para entender por que algumas rotas "somem"

## O que precisava ser feito para consertar

Existem duas formas seguras (podem ser usadas juntas):

### Opcao A (recomendada)
Colocar o app `produto` em prefixo explicito.

No arquivo `loja/urls.py`:
- trocar `path('', include('produto.urls'))`
- por `path('produto/', include('produto.urls'))`

Beneficio:
- elimina ambiguidade com rotas de outros apps.

### Opcao B
Manter o include de `produto` na raiz, mas garantir ordem correta e especificidade.

No arquivo `loja/urls.py`:
- deixar as rotas de `perfil/`, `pedido/`, `endereco/`, `carrinho_de_compras/`, `admin/` antes
- colocar `path('', include('produto.urls'))` por ultimo

No arquivo `produto/urls.py`:
- deixar rotas especificas antes
- manter `path('<slug:slug>/', ...)` sempre por ultimo

## Ajuste de consistencia no app produto

Em `produto/urls.py` havia:
- `path('produto/excluir/<int:produto_id>/', ...)`

Como o app ja e incluido externamente, esse caminho fica redundante dependendo da estrategia adotada.

Forma mais consistente dentro do app:
- `path('excluir/<int:produto_id>/', ...)`

## Resumo final

O erro principal nao era sintatico; era de desenho de rotas (rota generica competindo com rotas de outros apps).

Regra que evita esse problema no futuro:
- rotas especificas primeiro
- rotas genericas por ultimo
- preferir prefixos claros por app (`produto/`, `perfil/`, `pedido/` etc.)
