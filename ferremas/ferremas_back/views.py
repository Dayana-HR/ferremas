from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Carrito, ItemCarrito, Categoria, Producto
from .serializers import CarritoSerializer, CategoriaSerializer, ProductoSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from payment.views import crearTransaccion
from rest_framework import viewsets

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

@api_view(['POST', 'PUT'])
def agregar_producto_carrito(request):
    session_key = crear_session(request)
    id_producto = request.data.get('id_producto')
    cantidad = request.data.get('cantidad', 1)
    producto = get_object_or_404(Producto, id=id_producto)
    carrito, _ = Carrito.objects.get_or_create(session_key=session_key)

    item, fec_creacion = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    if request.method == 'PUT':
        cantidad_final = cantidad
    else:
        cantidad_final = (item.cantidad if not fec_creacion else 0) + cantidad
    if cantidad_final > producto.stock:
        return Response({
            'error': f'Stock insuficiente. Disponible: {producto.stock}, Solicitado: {cantidad_final}'
        }, status=400)
    if request.method == 'PUT':
        item.cantidad = cantidad
    else:
        if not fec_creacion:
            item.cantidad += cantidad
        else:
            item.cantidad = cantidad
    item.save()

    action = 'actualizado' if request.method == 'PUT' else 'agregado'
    return Response({
        'message': f'Producto {action} en el carrito',
        'cantidad_en_carrito': item.cantidad,
        'stock_disponible': producto.stock
    })


@api_view(['GET'])
def ver_carrito_por_session(request, session_key):
    carrito = get_object_or_404(Carrito, session_key=session_key)
    serializer = CarritoSerializer(carrito)
    return Response(serializer.data)

@api_view(['DELETE'])
def eliminar_carrito(request, producto_id, session_key):
    print("ENTRÓ A ELIMINAR CARRITO")
    carrito = get_object_or_404(Carrito, session_key=session_key)
    item = get_object_or_404(ItemCarrito, carrito=carrito, producto_id=producto_id)
    item.delete()
    return Response({'message': 'Producto eliminado del carrito'})

@api_view(['POST'])
def pagar_carrito(request):
    response = crearTransaccion(request._request) 
    if isinstance(response, HttpResponseRedirect):
        return response
    else:
        return Response(response, status=400)

# ViewSets para crear/ver productos y categorías desde Postman
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer