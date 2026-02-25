from django.db import models
from django.contrib.auth.models import User


class Pedido(models.Model):
    """
    Modelo para representar um pedido.
    """
    STATUS_CHOICES = (
        ('A', 'Aprovado'),
        ('C', 'Criado'),
        ('R', 'Reprovado'),
        ('P', 'Pendente'),
        ('E', 'Enviado'),
        ('F', 'Finalizado'),
    )

    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    total = models.FloatField()
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='C'
    )

    def __str__(self):
        return f'Pedido {self.id} - {self.get_status_display()}'


class ItemPedido(models.Model):
    """
    Modelo para representar um item do pedido.
    """
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.CharField(max_length=255)
    produto_id = models.PositiveIntegerField()
    variacao = models.CharField(max_length=255, null=True, blank=True)
    variacao_id = models.IntegerField(null=True, blank=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(null=True, blank=True)
    quantidade = models.IntegerField()
    imagem = models.CharField(max_length=2000)

    def __str__(self):
        return f'ItemPedido {self.id} - Pedido {self.pedido.id}'

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
