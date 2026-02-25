import re
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Endereco(models.Model):
    """
    class Endereco(models.Model):
    Modelo para representar um endereço associado a um perfil de usuário.
    """

    ESTADO_CHOICES = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    )

    perfil = models.ForeignKey(
        'perfil.Perfil', on_delete=models.CASCADE, related_name='enderecos'
    )
    cep = models.CharField(max_length=9)
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, blank=True)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES)

    def clean(self):
        """
        Valida o CEP para garantir que ele contenha apenas números e tenha 8 dígitos.
        """
        error_messages = {}

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            error_messages['cep'] = 'O CEP deve conter apenas números e ter 8 dígitos.'

        if error_messages:
            raise ValidationError(error_messages)

        def __str__(self):
            return f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade} - {self.estado}"

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"
