import sqlite3
from datetime import timezone as datetime_timezone
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management import BaseCommand, CommandError
from django.core.management.color import no_style
from django.db import connection, transaction
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime

from endereco.models import Endereco
from pedido.models import ItemPedido, Pedido
from perfil.models import Perfil
from produto.models import Categoria, ImportacaoLegada, Produto, Variacao


IMPORT_KEY = 'lojatech-sqlite-v1'
TABLE_MODELS = (
    ('auth_user', User),
    ('perfil_perfil', Perfil),
    ('endereco_endereco', Endereco),
    ('produto_categoria', Categoria),
    ('produto_produto', Produto),
    ('produto_variacao', Variacao),
    ('pedido_pedido', Pedido),
    ('pedido_itempedido', ItemPedido),
)


def read_rows(database, table):
    return [
        dict(row)
        for row in database.execute(f'SELECT * FROM "{table}" ORDER BY id')
    ]


def parse_legacy_datetime(value):
    if not value:
        return None
    parsed = parse_datetime(value)
    if parsed and timezone.is_naive(parsed):
        return timezone.make_aware(parsed, datetime_timezone.utc)
    return parsed


class Command(BaseCommand):
    help = 'Importa uma única vez os dados do SQLite legado para o banco atual.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            default=str(Path(settings.BASE_DIR) / 'db.sqlite3'),
            help='Caminho do SQLite de origem.',
        )
        parser.add_argument(
            '--media-root',
            default=str(Path(settings.BASE_DIR) / 'media'),
            help='Diretório das imagens legadas.',
        )
        parser.add_argument(
            '--merge',
            action='store_true',
            help='Permite importar quando o destino já contém dados.',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Repete uma importação que já possui marcador de conclusão.',
        )
        parser.add_argument(
            '--skip-media',
            action='store_true',
            help='Não envia arquivos para o storage configurado.',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Valida a origem e exibe as contagens sem alterar o destino.',
        )

    def handle(self, *args, **options):
        source = Path(options['source']).resolve()
        media_root = Path(options['media_root']).resolve()

        if not source.is_file():
            raise CommandError(f'SQLite de origem não encontrado: {source}')

        if connection.vendor == 'sqlite':
            destination = Path(connection.settings_dict['NAME']).resolve()
            if destination == source:
                raise CommandError('O SQLite de origem e o banco de destino são o mesmo arquivo.')

        with sqlite3.connect(source) as legacy:
            legacy.row_factory = sqlite3.Row
            integrity = legacy.execute('PRAGMA integrity_check').fetchone()[0]
            if integrity != 'ok':
                raise CommandError(f'Falha na integridade do SQLite: {integrity}')
            data = {
                table: read_rows(legacy, table)
                for table, _model in TABLE_MODELS
            }

        summary = {table: len(rows) for table, rows in data.items()}
        self.stdout.write(f'Origem íntegra: {source}')
        for table, count in summary.items():
            self.stdout.write(f'  {table}: {count}')

        if options['dry_run']:
            self.stdout.write(self.style.SUCCESS('Dry-run concluído; nenhuma alteração realizada.'))
            return

        previous = ImportacaoLegada.objects.filter(chave=IMPORT_KEY).first()
        if previous and not options['force']:
            self.stdout.write(
                self.style.WARNING(
                    f'Importação {IMPORT_KEY} já concluída em {previous.concluida_em}.'
                )
            )
            return

        destination_counts = {
            model._meta.label: model.objects.count()
            for _table, model in TABLE_MODELS
        }
        if any(destination_counts.values()) and not options['merge']:
            details = ', '.join(
                f'{label}={count}'
                for label, count in destination_counts.items()
                if count
            )
            raise CommandError(
                'O destino já contém dados. Revise antes de usar --merge: '
                f'{details}'
            )

        if not options['skip_media']:
            self.import_media(data['produto_produto'], media_root)

        with transaction.atomic():
            self.import_users(data['auth_user'])
            self.import_profiles(data['perfil_perfil'])
            self.import_addresses(data['endereco_endereco'])
            self.import_categories(data['produto_categoria'])
            self.import_products(data['produto_produto'])
            self.import_variations(data['produto_variacao'])
            self.import_orders(data['pedido_pedido'])
            self.import_order_items(data['pedido_itempedido'])
            self.reset_sequences()

            ImportacaoLegada.objects.update_or_create(
                chave=IMPORT_KEY,
                defaults={'resumo': summary},
            )

        self.stdout.write(self.style.SUCCESS('Dados legados importados com sucesso.'))

    def import_media(self, products, media_root):
        for row in products:
            relative_name = row.get('imagem')
            if not relative_name:
                continue
            source_file = media_root / Path(relative_name)
            if not source_file.is_file():
                raise CommandError(f'Imagem legada não encontrada: {source_file}')
            if default_storage.exists(relative_name):
                self.stdout.write(f'  mídia já existente: {relative_name}')
                continue
            with source_file.open('rb') as stream:
                saved_name = default_storage.save(relative_name, File(stream))
            if saved_name != relative_name:
                raise CommandError(
                    f'O storage alterou o nome de {relative_name} para {saved_name}.'
                )
            self.stdout.write(f'  mídia enviada: {relative_name}')

    def import_users(self, rows):
        for row in rows:
            User.objects.update_or_create(
                pk=row['id'],
                defaults={
                    'password': row['password'],
                    'last_login': parse_legacy_datetime(row['last_login']),
                    'is_superuser': row['is_superuser'],
                    'username': row['username'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'is_staff': row['is_staff'],
                    'is_active': row['is_active'],
                    'date_joined': parse_legacy_datetime(row['date_joined']),
                },
            )

    def import_profiles(self, rows):
        for row in rows:
            Perfil.objects.update_or_create(
                pk=row['id'],
                defaults={
                    'usuario_id': row['usuario_id'],
                    'data_nascimento': (
                        parse_date(row['data_nascimento'])
                        if row['data_nascimento']
                        else None
                    ),
                    'cpf': row['cpf'],
                    'telefone': row['telefone'],
                },
            )

    def import_addresses(self, rows):
        for row in rows:
            Endereco.objects.update_or_create(
                pk=row['id'],
                defaults={
                    'perfil_id': row['perfil_id'],
                    'cep': row['cep'],
                    'rua': row['rua'],
                    'numero': row['numero'],
                    'complemento': row['complemento'],
                    'bairro': row['bairro'],
                    'cidade': row['cidade'],
                    'estado': row['estado'],
                },
            )

    def import_categories(self, rows):
        for row in rows:
            Categoria.objects.update_or_create(
                pk=row['id'],
                defaults={'nome': row['nome'], 'slug': row['slug']},
            )

    def import_products(self, rows):
        for row in rows:
            Produto.objects.update_or_create(
                pk=row['id'],
                defaults={
                    'nome': row['nome'],
                    'categoria_id': row['categoria_id'],
                    'descricao_curta': row['descricao_curta'],
                    'descricao_longa': row['descricao_longa'],
                    'imagem': None,
                    'slug': row['slug'],
                    'preco_marketing': row['preco_marketing'],
                    'preco_marketing_promocional': row['preco_marketing_promocional'],
                    'tipo': row['tipo'],
                },
            )
            Produto.objects.filter(pk=row['id']).update(imagem=row['imagem'])

    def import_variations(self, rows):
        for row in rows:
            Variacao.objects.update_or_create(
                pk=row['id'],
                defaults={
                    'produto_id': row['produto_id'],
                    'nome': row['nome'],
                    'preco': row['preco'],
                    'preco_promocional': row['preco_promocional'],
                    'estoque': row['estoque'],
                },
            )

    def import_orders(self, rows):
        for row in rows:
            Pedido.objects.update_or_create(
                pk=row['id'],
                defaults={
                    'usuario_id': row['usuario_id'],
                    'total': row['total'],
                    'status': row['status'],
                },
            )

    def import_order_items(self, rows):
        for row in rows:
            ItemPedido.objects.update_or_create(
                pk=row['id'],
                defaults={
                    'pedido_id': row['pedido_id'],
                    'produto': row['produto'],
                    'produto_id': row['produto_id'],
                    'variacao': row['variacao'],
                    'variacao_id': row['variacao_id'],
                    'preco': row['preco'],
                    'preco_promocional': row['preco_promocional'],
                    'quantidade': row['quantidade'],
                    'imagem': row['imagem'],
                },
            )

    def reset_sequences(self):
        models = [model for _table, model in TABLE_MODELS]
        statements = connection.ops.sequence_reset_sql(no_style(), models)
        with connection.cursor() as cursor:
            for statement in statements:
                cursor.execute(statement)
