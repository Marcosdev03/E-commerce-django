from .models import Categoria


def categorias_nav(request):
    return {
        'categorias_nav': Categoria.objects.order_by('nome'),
    }
