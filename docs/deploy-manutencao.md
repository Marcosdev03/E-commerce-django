# Deploy e Manutencao

## Checklist para producao

- definir `DEBUG = False`
- configurar `ALLOWED_HOSTS`
- remover `debug_toolbar` de producao
- mover `SECRET_KEY` para variavel de ambiente
- configurar estrategia de static/media para servidor alvo
- habilitar logs de aplicacao e erros

## Qualidade e testes

Estado atual:

- existem arquivos `tests.py` nos apps
- ainda nao ha testes implementados

Recomendado:

1. cobrir fluxo de autenticacao e perfil
2. cobrir regras do carrinho e estoque
3. cobrir criacao e transicao de status do pedido
4. cobrir validacoes de CPF e CEP

## Melhorias tecnicas recomendadas

- criar `requirements.txt` ou `pyproject.toml`
- implementar endpoint de atualizacao de quantidade no carrinho
- revisar endpoint placeholder de exclusao em `produto/views.py`
- revisar internacionalizacao (`LANGUAGE_CODE`) para padrao Django

## Referencias internas

- Diagnostico de rotas: `DOCUMENTACAO_ERRO_URLS.md`
- Documento principal: `README.MD`
- Indice desta pasta: `docs/index.md`
