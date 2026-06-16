from decimal import Decimal
import json
import os
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import textwrap

from PIL import Image, ImageDraw, ImageFont


BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = BASE_DIR / 'media'

CATEGORIAS = {
    'Eletronicos': [
        'Smartphone', 'Notebook', 'Tablet', 'Fone Bluetooth', 'Smartwatch',
        'Camera Wi-Fi', 'Monitor LED', 'Teclado Mecanico', 'Mouse Gamer',
        'Caixa de Som'
    ],
    'Casa e Cozinha': [
        'Fritadeira Eletrica', 'Liquidificador', 'Cafeteira', 'Panela Antiaderente',
        'Jogo de Facas', 'Aspirador Portatil', 'Purificador de Agua',
        'Batedeira', 'Sanduicheira', 'Chaleira Eletrica'
    ],
    'Moda': [
        'Camiseta Premium', 'Calca Jeans', 'Jaqueta Corta Vento', 'Tenis Casual',
        'Mochila Urbana', 'Relogio Social', 'Oculos de Sol', 'Vestido Midi',
        'Camisa Polo', 'Carteira Couro'
    ],
    'Beleza e Saude': [
        'Secador de Cabelo', 'Massageador', 'Barbeador Eletrico', 'Kit Skincare',
        'Perfume', 'Escova Rotativa', 'Aparador', 'Protetor Solar',
        'Creme Hidratante', 'Modelador'
    ],
    'Esporte e Lazer': [
        'Bicicleta Urbana', 'Bola Oficial', 'Halter Emborrachado',
        'Garrafa Termica', 'Tapete Yoga', 'Mochila Trilhas', 'Patins',
        'Barraca Camping', 'Raquete', 'Corda de Pular'
    ],
    'Livros e Papelaria': [
        'Planner', 'Livro Tecnico', 'Caderno Executivo', 'Caneta Gel',
        'Estojo Organizador', 'Marcadores', 'Agenda', 'Mochila Escolar',
        'Calculadora', 'Luminaria de Mesa'
    ],
    'Brinquedos': [
        'Blocos de Montar', 'Boneca Articulada', 'Carrinho Controle Remoto',
        'Jogo Educativo', 'Quebra-Cabeca', 'Pelucia', 'Massinha',
        'Tabuleiro Familia', 'Drone Infantil', 'Kit Cientista'
    ],
    'Pet Shop': [
        'Cama Pet', 'Coleira Ajustavel', 'Bebedouro Automatico', 'Racao Premium',
        'Brinquedo Mordedor', 'Arranhador', 'Caixa Transporte',
        'Shampoo Pet', 'Escova Removedora', 'Comedouro Inox'
    ],
    'Ferramentas': [
        'Furadeira', 'Parafusadeira', 'Kit Chaves', 'Trena Digital',
        'Serra Tico-Tico', 'Martelo', 'Nivel Laser', 'Alicate Universal',
        'Caixa Ferramentas', 'Lanterna Recarregavel'
    ],
    'Games': [
        'Controle Sem Fio', 'Headset Gamer', 'Console Portatil', 'Mousepad RGB',
        'Cadeira Gamer', 'Jogo Aventura', 'Volante Simulador',
        'Carregador Duplo', 'Suporte Console', 'Teclado Compacto'
    ],
}

ADJETIVOS = [
    'Pro', 'Max', 'Prime', 'Plus', 'Ultra', 'Smart', 'Essencial', 'Comfort',
    'Studio', 'Active', 'Compact', 'Premium', 'Select', 'Flex', 'Neo'
]

PALETAS = [
    ('#1f2937', '#f97316', '#f8fafc'),
    ('#064e3b', '#22c55e', '#ecfdf5'),
    ('#7c2d12', '#facc15', '#fff7ed'),
    ('#0f766e', '#38bdf8', '#f0fdfa'),
    ('#4c1d95', '#f472b6', '#faf5ff'),
    ('#111827', '#ef4444', '#f9fafb'),
    ('#1e3a8a', '#a3e635', '#eff6ff'),
    ('#3f3f46', '#fb7185', '#fafafa'),
]


def main():
    total = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    env = carregar_env()
    database_url = env.get('DATABASE_URL')

    if not database_url:
        raise SystemExit('DATABASE_URL nao encontrado no .env.')

    random.seed(20260616)
    image_dir = MEDIA_ROOT / 'produto_imagens' / 'seed'
    image_dir.mkdir(parents=True, exist_ok=True)

    produtos = []
    categorias = list(CATEGORIAS)

    for indice in range(1, total + 1):
        categoria_nome = categorias[(indice - 1) % len(categorias)]
        lista_categoria = CATEGORIAS[categoria_nome]
        produto_base = lista_categoria[((indice - 1) // len(categorias)) % len(lista_categoria)]
        nome = f'{produto_base} {ADJETIVOS[(indice - 1) % len(ADJETIVOS)]} {100 + indice}'
        slug = f'catalogo-{indice:03d}-{slugify(nome)[:36]}'
        preco = preco_para(indice)
        promocional = preco_promocional_para(preco, indice)
        tipo = 'V' if indice % 4 else 'S'
        imagem_relativa = f'produto_imagens/seed/{slug}.jpg'

        criar_imagem(MEDIA_ROOT / imagem_relativa, nome, categoria_nome, indice)

        produtos.append({
            'indice': indice,
            'nome': nome,
            'categoria': categoria_nome,
            'categoria_slug': slugify(categoria_nome),
            'descricao_curta': descricao_curta(nome, categoria_nome),
            'descricao_longa': descricao_longa(nome, categoria_nome, indice),
            'imagem': imagem_relativa,
            'slug': slug,
            'preco': preco,
            'promocional': promocional,
            'tipo': tipo,
        })

    sql = montar_sql(produtos, categorias)

    with tempfile.NamedTemporaryFile('w', suffix='.sql', delete=False, encoding='utf-8') as arquivo:
        arquivo.write(sql)
        sql_path = arquivo.name

    try:
        comando = ['psql', database_url, '-v', 'ON_ERROR_STOP=1', '-f', sql_path]
        resultado = subprocess.run(comando)
        if resultado.returncode:
            raise SystemExit(f'psql falhou com codigo {resultado.returncode}.')
    finally:
        Path(sql_path).unlink(missing_ok=True)

    print(f'Seed concluido: {total} produtos, imagens e variacoes processados.')


def carregar_env():
    env = os.environ.copy()
    env_path = BASE_DIR / '.env'
    if not env_path.exists():
        return env

    for linha in env_path.read_text(encoding='utf-8').splitlines():
        linha = linha.strip()
        if not linha or linha.startswith('#') or '=' not in linha:
            continue
        chave, valor = linha.split('=', 1)
        env.setdefault(chave.strip(), valor.strip().strip('"').strip("'"))
    return env


def montar_sql(produtos, categorias):
    linhas = ['BEGIN;']

    for categoria in categorias:
        linhas.append(
            'INSERT INTO produto_categoria (nome, slug) VALUES '
            f'({literal(categoria)}, {literal(slugify(categoria))}) '
            'ON CONFLICT (nome) DO UPDATE SET slug = EXCLUDED.slug;'
        )

    for produto in produtos:
        linhas.append(
            'INSERT INTO produto_produto '
            '(nome, descricao_curta, descricao_longa, imagem, slug, '
            'preco_marketing, preco_marketing_promocional, tipo, categoria_id) '
            'VALUES ('
            f"{literal(produto['nome'])}, "
            f"{literal(produto['descricao_curta'])}, "
            f"{literal(produto['descricao_longa'])}, "
            f"{literal(produto['imagem'])}, "
            f"{literal(produto['slug'])}, "
            f"{produto['preco']}, "
            f"{produto['promocional']}, "
            f"{literal(produto['tipo'])}, "
            f"(SELECT id FROM produto_categoria WHERE nome = {literal(produto['categoria'])})"
            ') ON CONFLICT (slug) DO UPDATE SET '
            'nome = EXCLUDED.nome, '
            'descricao_curta = EXCLUDED.descricao_curta, '
            'descricao_longa = EXCLUDED.descricao_longa, '
            'imagem = EXCLUDED.imagem, '
            'preco_marketing = EXCLUDED.preco_marketing, '
            'preco_marketing_promocional = EXCLUDED.preco_marketing_promocional, '
            'tipo = EXCLUDED.tipo, '
            'categoria_id = EXCLUDED.categoria_id;'
        )

    slugs = ', '.join(literal(produto['slug']) for produto in produtos)
    linhas.append(
        'DELETE FROM produto_variacao '
        'WHERE produto_id IN (SELECT id FROM produto_produto WHERE slug IN '
        f'({slugs}));'
    )

    for produto in produtos:
        for variacao in variacoes_para(produto):
            linhas.append(
                'INSERT INTO produto_variacao '
                '(nome, preco, preco_promocional, estoque, produto_id) VALUES ('
                f"{literal(variacao['nome'])}, "
                f"{variacao['preco']}, "
                f"{variacao['promocional']}, "
                f"{variacao['estoque']}, "
                f"(SELECT id FROM produto_produto WHERE slug = {literal(produto['slug'])})"
                ');'
            )

    resumo = {
        'total_solicitado': len(produtos),
        'produtos_processados': len(produtos),
        'categorias': len(categorias),
        'imagens': len(produtos),
        'executor': 'scripts/popular_produtos_psql.py',
    }
    linhas.append(
        'INSERT INTO produto_importacaolegada (chave, concluida_em, resumo) VALUES '
        f"('seed_catalogo_500_produtos', NOW(), {literal(json.dumps(resumo))}::jsonb) "
        'ON CONFLICT (chave) DO UPDATE SET '
        'concluida_em = NOW(), resumo = EXCLUDED.resumo;'
    )

    linhas.append('COMMIT;')
    return '\n'.join(linhas)


def literal(valor):
    return "'" + str(valor).replace("'", "''") + "'"


def slugify(valor):
    texto = valor.lower()
    trocas = {
        ' ': '-', '_': '-', '/': '-', '.': '-', ',': '-', ':': '-',
    }
    resultado = []
    for caractere in texto:
        if caractere.isalnum():
            resultado.append(caractere)
        elif caractere in trocas:
            resultado.append('-')
    slug = ''.join(resultado)
    while '--' in slug:
        slug = slug.replace('--', '-')
    return slug.strip('-')


def preco_para(indice):
    reais = Decimal(29 + ((indice * 37) % 3970))
    centavos = Decimal((indice * 13) % 100) / Decimal('100')
    return (reais + centavos).quantize(Decimal('0.01'))


def preco_promocional_para(preco, indice):
    if indice % 3:
        return Decimal('0.00')
    desconto = Decimal('0.72') if indice % 2 else Decimal('0.84')
    return (preco * desconto).quantize(Decimal('0.01'))


def descricao_curta(nome, categoria):
    return (
        f'{nome} da categoria {categoria}, com acabamento moderno, '
        'boa disponibilidade em estoque e pronta entrega.'
    )


def descricao_longa(nome, categoria, indice):
    detalhes = [
        f'O {nome} foi selecionado para compor o catalogo de {categoria.lower()} com foco em custo-beneficio.',
        'Possui construcao confiavel, visual atual e especificacoes pensadas para uso diario.',
        'Produto cadastrado com imagens locais, categoria, precos, tipo de venda e variacoes para testes completos da loja.',
        f'Codigo interno do item: ECO-{indice:05d}.',
    ]
    return '\n\n'.join(detalhes)


def variacoes_para(produto):
    if produto['tipo'] == 'S':
        return [{
            'nome': 'Unico',
            'preco': produto['preco'],
            'promocional': produto['promocional'],
            'estoque': 8 + (produto['indice'] % 40),
        }]

    variacoes = []
    for posicao, nome in enumerate(['Padrao', 'Premium', 'Kit Completo']):
        acrescimo = Decimal(posicao * 35)
        preco = (produto['preco'] + acrescimo).quantize(Decimal('0.01'))
        promocional = Decimal('0.00')
        if produto['promocional']:
            promocional = (produto['promocional'] + acrescimo).quantize(Decimal('0.01'))
        variacoes.append({
            'nome': nome,
            'preco': preco,
            'promocional': promocional,
            'estoque': 5 + ((produto['indice'] + posicao) % 60),
        })
    return variacoes


def criar_imagem(path, nome, categoria, indice):
    if path.exists():
        return

    largura, altura = 900, 900
    fundo, destaque, texto = PALETAS[indice % len(PALETAS)]
    imagem = Image.new('RGB', (largura, altura), fundo)
    draw = ImageDraw.Draw(imagem)

    font_titulo = fonte(54)
    font_subtitulo = fonte(32)
    font_codigo = fonte(24)

    draw.rounded_rectangle((95, 110, 805, 705), radius=42, fill=texto)
    draw.rounded_rectangle((155, 180, 745, 620), radius=36, fill=destaque)
    draw.ellipse((275, 245, 625, 595), fill=fundo)
    draw.rounded_rectangle((335, 315, 565, 525), radius=26, fill=texto)
    draw.line((360, 370, 540, 370), fill=fundo, width=10)
    draw.line((360, 430, 540, 430), fill=fundo, width=10)
    draw.line((360, 490, 500, 490), fill=fundo, width=10)

    y = 735
    for linha in textwrap.wrap(nome, width=24)[:2]:
        draw.text((largura / 2, y), linha, fill=texto, font=font_titulo, anchor='mm')
        y += 58

    draw.text((largura / 2, 845), categoria, fill=destaque, font=font_subtitulo, anchor='mm')
    draw.text((largura - 44, 44), f'ECO-{indice:05d}', fill=texto, font=font_codigo, anchor='ra')

    imagem.save(path, format='JPEG', quality=88, optimize=True)


def fonte(tamanho):
    caminhos = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf',
    ]
    for caminho in caminhos:
        if Path(caminho).exists():
            return ImageFont.truetype(caminho, tamanho)
    return ImageFont.load_default()


if __name__ == '__main__':
    main()
