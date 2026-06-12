from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0006_categoria_produto_categoria'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportacaoLegada',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('chave', models.CharField(max_length=100, unique=True)),
                ('concluida_em', models.DateTimeField(auto_now_add=True)),
                ('resumo', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'verbose_name': 'Importação legada',
                'verbose_name_plural': 'Importações legadas',
            },
        ),
    ]
