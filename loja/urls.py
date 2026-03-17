"""
URL configuration for loja project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.urls import re_path
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [

    path('admin/', admin.site.urls),
    path('perfil/', include('perfil.urls')),
    path('pedido/', include('pedido.urls')),
    path('endereco/', include('endereco.urls')),
    path('carrinho_de_compras/', include('carrinho_de_compras.urls')),
    path('', include('produto.urls')),
    
    

]


# TODO: 'REMOVER debug_toolbar em produção'
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# In this deployment, media requests can arrive either as /media/... or
# /ecomecer/media/... depending on proxy routing. Keep both mapped.
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.FORCE_SCRIPT_NAME:
    script_prefix = settings.FORCE_SCRIPT_NAME.strip('/')
    urlpatterns += [
        re_path(rf'^{script_prefix}/media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]