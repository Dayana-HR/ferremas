from django.shortcuts import render
from ferremas_back.models import Producto

# Create your views here.
def vista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'index.html', {'productos': productos})

def vista_carrito_html(request):
    return render(request, 'carrito.html')

def pago_confirmado(request):
    return render(request, 'confirmado.html')
