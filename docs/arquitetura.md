# Arquitetura

## Apps do projeto

- `produto`: catalogo, categorias, variacoes, listagem e detalhe
- `carrinho_de_compras`: carrinho em sessao
- `perfil`: cadastro, login/logout e atualizacao do usuario
- `endereco`: cadastro, edicao e exclusao de endereco
- `pedido`: criacao e acompanhamento de pedidos
- `utils`: funcoes de apoio (validacao CPF, formatacao de preco)

## Estrutura principal

```text
loja/                  # Configuracao global (settings e urls)
produto/               # Catalogo
carrinho_de_compras/   # Carrinho
perfil/                # Conta
endereco/              # Endereco de entrega
pedido/                # Pedido e itens
templates/             # Base e parciais globais
utils/                 # Utilitarios
media/                 # Uploads
static/                # Arquivos estaticos
```

## Configuracoes de destaque

Arquivo: `loja/settings.py`

- Banco: SQLite (`db.sqlite3`)
- Templates globais em `templates/`
- Context processors customizados:
  - `carrinho_de_compras.context_processors.quantidade_total_carrinho`
  - `produto.context_processors.categorias_nav`
- Sessao configurada para 7 dias (`SESSION_COOKIE_AGE`)
- `debug_toolbar` habilitado em desenvolvimento
