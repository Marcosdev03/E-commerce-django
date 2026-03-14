"""
Admin do produto
"""
from . import models
from django import forms
from django.contrib import admin


class VariacaoForm(forms.ModelForm):
    """
    Formulário para exibir as variações do produto
    na página de administração do produto.
    """
    class Meta:
        model = models.Variacao
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in ['preco', 'preco_promocional']:
            self.fields[campo].localize = True


class VariacaoInline(admin.TabularInline):
    """
    Classe para exibir as variações do produto
    na página de administração do produto.
    """
    model = models.Variacao
    form = VariacaoForm
    extra = 1


class ProdutoAdmin(admin.ModelAdmin):
    """
    Classe para exibir o produto na página de administração do produto.
    """
    inlines = [
        VariacaoInline
    ]

    list_display = ['nome', 'get_preco_formatado',
                    'get_preco_promocional_formatado', 'tipo', 'categoria']
    list_filter = ['tipo', 'categoria']
    search_fields = ['nome', 'descricao_curta']

    @admin.display(description='Preço')
    def get_preco_formatado(self, obj):
        """
        Método para exibir o preço formatado do produto na página de administração do produto.
        """
        return obj.get_preco_formatado()

    @admin.display(description='Preço Promocional')
    def get_preco_promocional_formatado(self, obj):
        """
        Método para exibir o preço promocional formatado
        do produto na página de administração do produto.
        """
        return obj.get_preco_promocional_formatado()


admin.site.register(models.Produto, ProdutoAdmin)
admin.site.register(models.Variacao)
admin.site.register(models.Categoria)
