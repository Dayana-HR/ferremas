from django.shortcuts import render
from .models import Producto
from .serializers import ProductoSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
def getStock(request, id):
    try:
        producto = Producto.objects.get(id=id)
        if producto.stock <= 0:
            return Response({"error": "No hay stock disponible"}, status=404)
            
        serializer = ProductoSerializer(producto, many=False)
        return Response(serializer.data)
    except Producto.DoesNotExist:
        return Response({"error": f"Producto con ID {id} no encontrado"}, status=404)
    except Exception as e:
        return Response({"error": "Error no controlado"}, status=500)

