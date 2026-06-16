from decimal import Decimal
from pathlib import Path
import random
import textwrap

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from PIL import Image, ImageDraw, ImageFont

from produto.models import Categoria, ImportacaoLegada, Produto, Variacao


class Command(BaseCommand):
    help = 'Popula a loja com produtos, categorias, variacoes e imagens locais.'

    categorias = {
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

    adjetivos = [
        'Pro', 'Max', 'Prime', 'Plus', 'Ultra', 'Smart', 'Essencial', 'Comfort',
        'Studio', 'Active', 'Compact', 'Premium', 'Select', 'Flex', 'Neo'
    ]

    paletas = [
        ('#1f2937', '#f97316', '#f8fafc'),
        ('#064e3b', '#22c55e', '#ecfdf5'),
        ('#7c2d12', '#facc15', '#fff7ed'),
        ('#0f766e', '#38bdf8', '#f0fdfa'),
        ('#4c1d95', '#f472b6', '#faf5ff'),
        ('#111827', '#ef4444', '#f9fafb'),
        ('#1e3a8a', '#a3e635', '#eff6ff'),
        ('#3f3f46', '#fb7185', '#fafafa'),
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=500,
            help='Quantidade de produtos a criar ou atualizar.',
        )

    def handle(self, *args, **options):
        total = options['total']
        random.seed(20260616)

        categorias = {
            nome: Categoria.objects.get_or_create(nome=nome)[0]
            for nome in self.categorias
        }

        image_dir = Path(settings.MEDIA_ROOT) / 'produto_imagens' / 'seed'
        image_dir.mkdir(parents=True, exist_ok=True)

        criados = 0
        atualizados = 0

        for indice in range(1, total + 1):
            categoria_nome = list(self.categorias)[(indice - 1) % len(self.categorias)]
            categoria = categorias[categoria_nome]
            produto_base = self.categorias[categoria_nome][
                ((indice - 1) // len(self.categorias)) % len(self.categorias[categoria_nome])
            ]
            adjetivo = self.adjetivos[(indice - 1) % len(self.adjetivos)]
            modelo = 100 + indice
            nome = f'{produto_base} {adjetivo} {modelo}'
            slug = f'catalogo-{indice:03d}-{slugify(nome)[:36]}'
            preco = self._preco_para(indice)
            promocional = self._preco_promocional_para(preco, indice)
            tipo = 'V' if indice % 4 else 'S'
            imagem_relativa = f'produto_imagens/seed/{slug}.jpg'
            imagem_path = Path(settings.MEDIA_ROOT) / imagem_relativa

            self._criar_imagem(imagem_path, nome, categoria_nome, indice)

            produto, created = Produto.objects.update_or_create(
                slug=slug,
                defaults={
                    'nome': nome,
                    'categoria': categoria,
                    'descricao_curta': self._descricao_curta(nome, categoria_nome),
                    'descricao_longa': self._descricao_longa(nome, categoria_nome, indice),
                    'imagem': imagem_relativa,
                    'preco_marketing': preco,
                    'preco_marketing_promocional': promocional,
                    'tipo': tipo,
                },
            )

            Variacao.objects.filter(produto=produto).delete()
            self._criar_variacoes(produto, preco, promocional, tipo)

            if created:
                criados += 1
            else:
                atualizados += 1

        ImportacaoLegada.objects.update_or_create(
            chave='seed_catalogo_500_produtos',
            defaults={
                'resumo': {
                    'total_solicitado': total,
                    'produtos_criados': criados,
                    'produtos_atualizados': atualizados,
                    'categorias': len(categorias),
                    'imagens': total,
                }
            },
        )

        self.stdout.write(self.style.SUCCESS(
            f'Seed concluido: {criados} produtos criados, '
            f'{atualizados} atualizados, {total} imagens geradas.'
        ))

    def _preco_para(self, indice):
        reais = Decimal(29 + ((indice * 37) % 3970))
        centavos = Decimal((indice * 13) % 100) / Decimal('100')
        return (reais + centavos).quantize(Decimal('0.01'))

    def _preco_promocional_para(self, preco, indice):
        if indice % 3:
            return Decimal('0.00')
        desconto = Decimal('0.72') if indice % 2 else Decimal('0.84')
        return (preco * desconto).quantize(Decimal('0.01'))

    def _descricao_curta(self, nome, categoria):
        return (
            f'{nome} da categoria {categoria}, com acabamento moderno, '
            'boa disponibilidade em estoque e pronta entrega.'
        )

    def _descricao_longa(self, nome, categoria, indice):
        detalhes = [
            f'O {nome} foi selecionado para compor o catalogo de {categoria.lower()} com foco em custo-beneficio.',
            'Possui construcao confiavel, visual atual e especificacoes pensadas para uso diario.',
            'Produto cadastrado com imagens locais, categoria, precos, tipo de venda e variacoes para testes completos da loja.',
            f'Codigo interno do item: ECO-{indice:05d}.',
        ]
        return '\n\n'.join(detalhes)

    def _criar_variacoes(self, produto, preco, promocional, tipo):
        if tipo == 'S':
            Variacao.objects.create(
                produto=produto,
                nome='Unico',
                preco=float(preco),
                preco_promocional=float(promocional),
                estoque=8 + (produto.id % 40),
            )
            return

        opcoes = ['Padrao', 'Premium', 'Kit Completo']
        for posicao, nome in enumerate(opcoes):
            acrescimo = Decimal(posicao * 35)
            preco_variacao = (preco + acrescimo).quantize(Decimal('0.01'))
            if promocional:
                promocional_variacao = (promocional + acrescimo).quantize(Decimal('0.01'))
            else:
                promocional_variacao = Decimal('0.00')

            Variacao.objects.create(
                produto=produto,
                nome=nome,
                preco=float(preco_variacao),
                preco_promocional=float(promocional_variacao),
                estoque=5 + ((produto.id + posicao) % 60),
            )

    def _criar_imagem(self, path, nome, categoria, indice):
        if path.exists():
            return

        largura, altura = 900, 900
        fundo, destaque, texto = self.paletas[indice % len(self.paletas)]
        imagem = Image.new('RGB', (largura, altura), fundo)
        draw = ImageDraw.Draw(imagem)

        font_titulo = self._fonte(54)
        font_subtitulo = self._fonte(32)
        font_codigo = self._fonte(24)

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

    def _fonte(self, tamanho):
        caminhos = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
            '/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf',
        ]
        for caminho in caminhos:
            if Path(caminho).exists():
                return ImageFont.truetype(caminho, tamanho)
        return ImageFont.load_default()
