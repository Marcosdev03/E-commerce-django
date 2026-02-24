"""
Admin do produto
"""
from django.contrib import admin
from .models import Produto

admin.site.register(Produto)
