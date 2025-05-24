from django.shortcuts import render
from .models import Producto
from .serializers import ProductoSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
def getStock(request):
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    print(serializer)
    return Response(serializer.data)

