# Modelos de Dados

## Produto (`produto/models.py`)

### Categoria

- `nome`
- `slug`
- Gera slug automaticamente no `save`.

### Produto

- `nome`
- `categoria` (FK para `Categoria`)
- `descricao_curta`
- `descricao_longa`
- `imagem`
- `slug`
- `preco_marketing`
- `preco_marketing_promocional`
- `tipo` (`V` variavel, `S` simples)

Regras:

- gera slug no `save` quando vazio
- redimensiona imagem para largura maxima de 800 px

### Variacao

- `produto` (FK)
- `nome`
- `preco`
- `preco_promocional`
- `estoque`

## Perfil (`perfil/models.py`)

### Perfil

- `usuario` (OneToOne com `auth.User`)
- `data_nascimento`
- `cpf`
- `telefone`

Regras:

- valida CPF usando `utils.validacpf.valida_cpf`
- propriedade `idade` calculada por data de nascimento

## Endereco (`endereco/models.py`)

### Endereco

- `perfil` (FK para `perfil.Perfil` com `related_name='enderecos'`)
- `cep`
- `rua`
- `numero`
- `complemento`
- `bairro`
- `cidade`
- `estado`

Regras:

- validacao de CEP no model
- `EnderecoForm.clean_cep` normaliza para 8 digitos

## Pedido (`pedido/models.py`)

### Pedido

- `usuario` (FK)
- `total`
- `status`

Status mapeados:

- `A`: aprovado
- `C`: criado
- `R`: reprovado
- `P`: pendente
- `E`: enviado
- `F`: finalizado

### ItemPedido

- `pedido` (FK)
- `produto`
- `produto_id`
- `variacao`
- `variacao_id`
- `preco`
- `preco_promocional`
- `quantidade`
- `imagem`

Observacao:

`ItemPedido` funciona como snapshot dos dados do item no momento da compra.
