from django.contrib import admin

from .models import Producto, Categoria, Carrito, ItemCarrito

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'marca', 'categoria', 'stock')
    search_fields = ('id','nombre', 'marca')
    list_filter = ('categoria', 'marca')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('id', 'nombre')
    list_filter = ('id', 'nombre')

@admin.register(Carrito)
class Carrito(admin.ModelAdmin):
    list_display = ('session_key', 'fec_creacion')
    
@admin.register(ItemCarrito)
class ItemCarrito(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'cantidad')

