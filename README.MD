# E-commerce Django

Projeto de e-commerce desenvolvido com Django, com fluxo completo de:

- catálogo de produtos por categoria
- busca de produtos
- carrinho em sessão
- cadastro/autenticação de usuário
- cadastro de endereço
- criação e acompanhamento de pedidos

Data de início informada no repositório: `21/02/2026`.

Versao modular desta documentacao: `docs/index.md`.

## 1. Visão geral

O sistema é dividido em apps Django com responsabilidades separadas:

- `produto`: catálogo, categorias, variações e listagem/detalhe
- `carrinho_de_compras`: gestão do carrinho via sessão
- `perfil`: cadastro, login/logout e atualização de dados do usuário
- `endereco`: CRUD de endereços de entrega por usuário
- `pedido`: criação do pedido a partir do carrinho e avanço de status
- `utils`: utilitários (ex.: validação de CPF e formatação monetária)

## 2. Stack e tecnologias

- Python 3.x
- Django `4.2.11`
- SQLite (`db.sqlite3`)
- Bootstrap + Font Awesome (assets estáticos locais)
- Pillow (redimensionamento de imagem de produto)
- Django Debug Toolbar (ativo em desenvolvimento)

## 3. Estrutura principal

```text
loja/                  # Configuração global (settings, urls)
produto/               # Catálogo, categorias e variações
carrinho_de_compras/   # Carrinho em sessão
perfil/                # Usuário e perfil
endereco/              # Endereços do usuário
pedido/                # Pedido e itens do pedido
templates/             # Base e parciais globais
utils/                 # Funções utilitárias
media/                 # Upload de imagens
static/                # Arquivos estáticos coletados
```

## 4. Configuração do ambiente

Como não há `requirements.txt` no repositório, instale manualmente as dependências mínimas.

### 4.1. Criar e ativar ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4.2. Instalar dependências

```bash
pip install django==4.2.11 pillow django-debug-toolbar
```

### 4.3. Aplicar migrações

```bash
python manage.py migrate
```

### 4.4. Criar superusuário (opcional)

```bash
python manage.py createsuperuser
```

### 4.5. Rodar servidor

```bash
python manage.py runserver
```

Aplicação: `http://127.0.0.1:8000/`

Admin: `http://127.0.0.1:8000/admin/`

Debug Toolbar (quando `DEBUG=True`): `http://127.0.0.1:8000/__debug__/`

## 5. Configurações importantes (`loja/settings.py`)

- `INSTALLED_APPS` inclui: `pedido`, `perfil`, `produto`, `endereco`, `carrinho_de_compras`, `debug_toolbar`
- Banco padrão: SQLite (`db.sqlite3`)
- Templates globais em `templates/`
- Context processors customizados:
	- `carrinho_de_compras.context_processors.quantidade_total_carrinho`
	- `produto.context_processors.categorias_nav`
- Arquivos de mídia:
	- `MEDIA_URL = '/media/'`
	- `MEDIA_ROOT = .../media`
- Sessão:
	- `SESSION_COOKIE_AGE = 7 dias`

## 6. Rotas do projeto

Rotas globais em `loja/urls.py`:

- `/admin/` -> admin Django
- `/perfil/` -> app `perfil`
- `/pedido/` -> app `pedido`
- `/endereco/` -> app `endereco`
- `/carrinho_de_compras/` -> app `carrinho_de_compras`
- `/` -> app `produto`

### 6.1. App `produto`

- `GET /` -> lista de produtos (`produto:lista`)
- `GET /<slug>/` -> detalhe de produto (`produto:detalhe`)
- `GET /excluir/<slug>/` -> endpoint placeholder (`produto:excluir`)

Filtros da listagem por query string:

- `?categoria=<slug_da_categoria>`
- `?q=<termo_de_busca>`

### 6.2. App `perfil`

- `GET|POST /perfil/` -> cadastro de usuário/perfil (`perfil:perfil`)
- `GET|POST /perfil/atualizar/` -> atualizar conta (`perfil:atualizar`)
- `GET|POST /perfil/login/` -> autenticação (`perfil:login`)
- `GET /perfil/logout/` -> logout (`perfil:logout`)

### 6.3. App `endereco`

- `GET|POST /endereco/` -> novo endereço (`endereco:inicio`)
- `GET|POST /endereco/novo/` -> novo endereço (`endereco:novo`)
- `GET|POST /endereco/editar/<pk>/` -> editar (`endereco:editar`)
- `GET|POST /endereco/excluir/<pk>/` -> excluir (`endereco:excluir`)

### 6.4. App `carrinho_de_compras`

- `GET /carrinho_de_compras/` -> visualiza carrinho (`carrinho_de_compras:carrinho`)
- `GET /carrinho_de_compras/adicionaraocarrinho/?vid=<variacao_id>` -> adiciona item
- `GET /carrinho_de_compras/removerdocarrinho/?vid=<variacao_id>` -> remove item
- `GET /carrinho_de_compras/atualizar/` -> endpoint placeholder

### 6.5. App `pedido`

- `GET /pedido/` -> resumo para pagamento (`pedido:pagar`)
- `GET /pedido/fecharpedido/<pedido_id>/` -> avança status (`pedido:fechar-pedido`)
- `GET /pedido/detalhe/<pedido_id>/` -> detalhe do pedido (`pedido:detalhe`)

## 7. Modelos e domínio

## 7.1. `produto.models`

- `Categoria`
	- `nome`, `slug`
	- `slug` gerado automaticamente com `slugify` no `save`
- `Produto`
	- `nome`, `categoria`, descrições curta/longa, imagem, `slug`
	- preços: `preco_marketing`, `preco_marketing_promocional`
	- `tipo`: variável (`V`) ou simples (`S`)
	- no `save`: gera `slug` e redimensiona imagem (largura máx. 800px)
- `Variacao`
	- vinculada a `Produto`
	- `nome`, `preco`, `preco_promocional`, `estoque`

## 7.2. `perfil.models`

- `Perfil`
	- `OneToOne` com `User`
	- `data_nascimento`, `cpf`, `telefone`
	- valida CPF com `utils.validacpf.valida_cpf`
	- propriedade `idade`

## 7.3. `endereco.models`

- `Endereco`
	- `ForeignKey` para `perfil.Perfil` (`related_name='enderecos'`)
	- `cep`, `rua`, `numero`, `complemento`, `bairro`, `cidade`, `estado`
	- validação de CEP e formulário normaliza para 8 dígitos

## 7.4. `pedido.models`

- `Pedido`
	- `usuario`, `total`, `status`
	- status possíveis: `A`, `C`, `R`, `P`, `E`, `F`
- `ItemPedido`
	- snapshot do item comprado (`produto`, `variacao`, `precos`, `quantidade`, `imagem`)

## 8. Fluxo funcional do usuário

## 8.1. Catálogo

1. Usuário entra em `/`.
2. Pode buscar por texto (`q`) e filtrar por categoria.
3. Acessa o detalhe pelo slug do produto.

## 8.2. Carrinho

1. No detalhe do produto, escolhe variação (`vid`) e adiciona ao carrinho.
2. Carrinho é salvo em `request.session['carrinho']`.
3. Controle de estoque evita quantidade acima do disponível.

Estrutura de cada item em sessão (resumo):

- `produto_id`, `produto_nome`
- `variacao_id`, `variacao_nome`
- `preco_unitario`, `preco_unitario_promocional`
- `preco_quantitativo`, `preco_quantitativo_promocional`
- `quantidade`, `slug`, `imagem`

## 8.3. Conta e endereço

1. Usuário cria conta em `/perfil/`.
2. Faz login em `/perfil/login/`.
3. Gerencia dados pessoais e endereços em `/perfil/atualizar/`.

## 8.4. Pedido

1. Em `/pedido/`, o sistema exige usuário logado, carrinho não vazio e endereço cadastrado.
2. Se não houver pedido aberto (`status='C'`), cria a partir do carrinho.
3. Ao fechar pedido:
	 - `C` -> `P` (enviado para processamento)
	 - `P` -> `F` (finalizado)
4. Sessão limpa `pedido_id` e carrinho quando apropriado.

## 9. Context processors e templates

- `quantidade_total_carrinho`: soma quantidades para mostrar no menu
- `categorias_nav`: carrega categorias para dropdown da navbar

Templates globais:

- `templates/base.html` estrutura principal
- `templates/parciais/_nav.html` navegação, busca e acesso ao carrinho
- `templates/parciais/_messages.html` feedback de ações com `messages`

## 10. Admin e dados

Use `/admin/` para:

- cadastrar categorias, produtos e variações
- gerenciar usuários/perfis
- acompanhar pedidos e itens

Recomendação de ordem para popular ambiente de desenvolvimento:

1. criar categorias
2. criar produtos
3. criar variações com estoque
4. criar usuário e endereço
5. simular compra no front

## 11. Qualidade, testes e observações

- Arquivos `tests.py` dos apps existem, porém ainda sem testes implementados.
- Projeto contém observações para remover `debug_toolbar` em produção.
- Existe documentação de diagnóstico de rotas em `DOCUMENTACAO_ERRO_URLS.md`.

## 12. Pontos de atenção para produção

Antes de publicar:

- definir `DEBUG = False`
- configurar `ALLOWED_HOSTS`
- remover `debug_toolbar` de produção
- proteger `SECRET_KEY` com variável de ambiente
- revisar estratégia de arquivos estáticos e mídia
- adicionar suíte de testes

## 13. Melhorias sugeridas

- Criar `requirements.txt` ou `pyproject.toml`
- Implementar atualização de quantidade no carrinho (`AtualizarProdutoDoCarrinho`)
- Revisar endpoint de exclusão de produto (placeholder)
- Cobrir fluxos críticos com testes automatizados
- Ajustar internacionalização (`LANGUAGE_CODE`) conforme padrão Django (`pt-br`)

## 14. Comandos úteis

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python manage.py test
```

---

Se quiser, posso também gerar uma versão em `docs/` com separação por capítulos (`arquitetura.md`, `rotas.md`, `modelo-dados.md`, `deploy.md`) para ficar mais organizado para equipe.