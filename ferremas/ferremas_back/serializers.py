from rest_framework import serializers
from .models import ItemCarrito,Categoria, Producto, Carrito


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    categoria = serializers.SlugRelatedField(
        queryset=Categoria.objects.all(),
        slug_field='id'
    )
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'marca', 'stock', 'precio', 'cod_ext', 'fec_modif', 'categoria']

class ItemCarritoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)

    class Meta: 
        model = ItemCarrito
        fields = ['id', 'producto', 'cantidad']

class CarritoSerializer(serializers.ModelSerializer):
    items = ItemCarritoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Carrito
        fields = ['id', 'session_key', 'fec_creacion', 'items', 'total']