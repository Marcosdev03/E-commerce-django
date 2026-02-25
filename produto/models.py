"""
Módulo responsável pelos modelos da aplicação Produto.
"""
import os
from PIL import Image
from django.db import models
from django.conf import settings


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
        """
        Metodo para redimensionar a imagem do produto, garantindo que ela não 
        ultrapasse a largura máxima definida.
        """

        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        if original_width <= new_width:
            print('Retornando, largura menor que a nova largura.')
            img_pil.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(img_full_path, quality=70, optimize=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

    def __str__(self):
        return self.nome


class Variacao(models.Model):
    """
    Modelo de Variação, representando uma variação de um produto.
    """

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
