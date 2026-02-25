from datetime import date
from django.db import models
from utils.validacpf import valida_cpf
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Perfil(models.Model):
    """
    Modelo para representar um perfil de usuário.
    """
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Usuário')
    data_nascimento = models.DateField(null=True, blank=True)
    cpf = models.CharField(max_length=14, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username

    def clean(self):
        """
        Valida o CPF para garantir que ele tenha exatamente 11 dígitos.
        """
        error_messages = {}

        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Digite um CPF válido.'

        if error_messages:
            raise ValidationError(error_messages)

    @property
    def idade(self):
        """
        Calcula a idade do usuário com base na data de nascimento."""
        if not self.data_nascimento:
            return None
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (
                self.data_nascimento.month, self.data_nascimento.day)
        )

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
