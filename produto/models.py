"""
Módulo responsável pelos modelos da aplicação Produto.
"""
from django.db import models


class Produto(models.Model):
    """
    Modelo de Produto, representando um produto no sistema.
    """

    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(
        upload_to='produto_imagens/%y/%m/', blank=True, null=True)
    slug = models.SlugField(unique=True)
    preco_marketing = models.DecimalField(decimal_places=2, max_digits=10)
    preco_marketing_promocional = models.DecimalField(
        default=0, decimal_places=2, max_digits=10)
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variação'),
            ('S', 'Simples'),
        )
    )

    @staticmethod
    def resize_image(img, new_width=800):
        print(img.name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

    def __str__(self):
        return self.nome
