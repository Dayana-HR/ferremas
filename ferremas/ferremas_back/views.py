from django.shortcuts import get_object_or_404, render
from .models import Carrito, ItemCarrito, Producto
from .serializers import CarritoSerializer, ProductoSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
def getStock(request):
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    print(serializer)
    return Response(serializer.data)

def crear_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

@api_view(['GET'])
def ver_carrito(request):
    session_key = crear_session(request)
    carrito, _ = Carrito.objects.get_or_create(session_key=session_key)
    serializer = CarritoSerializer(carrito)
    return Response(serializer.data)

@api_view(['POST'])
def agregar_producto_carrito(request):
    session_key = crear_session(request)
    id_producto = request.data.get('id_producto')
    cantidad = request.data.get('cantidad', 1)
    producto = get_object_or_404(Producto, id=id_producto)
    carrito, _ = Carrito.objects.get_or_create(session_key=session_key)

    item, fec_creacion = ItemCarrito.objects.get_or_create(carrito= carrito, producto=producto)
    if not fec_creacion:
        item.cantidad += cantidad
    else:
        item.cantidad = cantidad
    item.save()
    return Response({'message': 'Producto agregado al carrito'})

@api_view(['GET'])
def ver_carrito_por_session(request, session_key):
    carrito = get_object_or_404(Carrito, session_key=session_key)
    serializer = CarritoSerializer(carrito)
    return Response(serializer.data)

@api_view(['DELETE'])
def eliminar_carrito(request, producto_id, session_key):
    print("ENTRÓ A ELIMINAR CARRITO")
    # session_key = crear_session(request)
    carrito = get_object_or_404(Carrito, session_key=session_key)
    item = get_object_or_404(ItemCarrito, carrito=carrito, producto_id=producto_id)
    item.delete()
    return Response({'message': 'Producto eliminado del carrito'})



