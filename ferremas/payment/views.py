import json
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from ferremas_back.models import Carrito, ItemCarrito, Producto
from ferremas_back.serializers import CarritoSerializer, ProductoSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib import messages
from django.conf import settings
import requests
from django.db import transaction

# Create your views here.

# Recibe GET o POST y obtiene el carrito asociado a la sesion y crea la transacción en Webpay
@api_view(['GET', 'POST'])
def crearTransaccion(request):
    # Obtiene o crea la session_key para identificar el carrito
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    # Obtiene el carrito correspondiente a la session_key
    carrito = get_object_or_404(Carrito, session_key=session_key)
    serializer = CarritoSerializer(carrito)
    carrito_data = serializer.data

    # Datos necesarios por webpay para la transaccion
    buy_order = carrito_data['id']
    session_id = session_key
    amount = float(carrito_data['total'])

    # URL a la que Webpay redireccionara al finalizar el pago
    ruta = request.build_absolute_uri(reverse('webpay_respuesta'))

    # Datos que se enviaran a Webpay para crear la transacción
    payload = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": ruta
    }

    # Se realiza la llamada a Webpay para crear la transacción
    payment_response = pagarConWebpay(payload)

    if payment_response:

        # Si se crea con exito se guarda el token en el carrito
        token_ws = payment_response.get("token")
        url = payment_response.get("url")
        carrito.token_ws = token_ws
        carrito.save(update_fields=['token_ws'])

        # Se redirige al usuario a la URL de pago en Webpay con el token_ws
        return HttpResponseRedirect(f"{url}?token_ws={token_ws}")
    else:
        messages.error(request, "Hubo un problema al procesar el pago. Intenta nuevamente.")
        return redirect('vercarrito')

# Envia POST al endpoint de Webpay para crear la transaccion
def pagarConWebpay(payload):
    endpoint = settings.WEBPAY_BASE_URL + "/rswebpaytransaction/api/webpay/v1.2/transactions"
    headers = {
        'Tbk-Api-Key-Id': settings.WEBPAY_COMMERCE_CODE,
        'Tbk-Api-Key-Secret': settings.WEBPAY_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.post(endpoint, json=payload, headers=headers)

    if response.status_code == 200:
        respuesta = json.loads(response.text)
        # Retorna token y url para el pago
        return {
            'token': respuesta.get('token'),
            'url': respuesta.get('url')
        } 
        
    else:
        print(f"Error al procesar el pago: {response.status_code} - {response.text}")
        return None

# Se consulta el estado del pago en Webpay usando el token_ws recibido
def obtener_estado_pago_webpay(token):
    url = settings.WEBPAY_BASE_URL + f"/rswebpaytransaction/api/webpay/v1.2/transactions/{token}"

    headers = {
        'Tbk-Api-Key-Id': settings.WEBPAY_COMMERCE_CODE,
        'Tbk-Api-Key-Secret': settings.WEBPAY_API_KEY,
        'Content-Type': 'application/json'
    }
    try:
        # Hace el PUT para obtener el estado
        response = requests.put(url, headers=headers) 
        return response.json()
    except Exception as e:
        print("Error al obtener estado:", e)
        return None

#Vista que recibe la respuesta de Webpay luego del pago
@api_view(['GET', 'POST'])
def webpay_respuesta(request):
    token_ws = request.GET.get('token_ws') or request.POST.get('token_ws')
    if not token_ws:
        return render(request, 'token_fallido.html', {'error': 'token inválido'})
    
    # Consulta el estado del pago en Webpay
    resultado = obtener_estado_pago_webpay(token_ws)
    if resultado:
        estado = resultado.get('status')
        if estado == 'AUTHORIZED':
            try:
                carrito = Carrito.objects.get(token_ws=token_ws)
            except Carrito.DoesNotExist:
                carrito = None
            if carrito:
                #Si falla la actualizacion en algun producto no se guarda ninguna actualizacion
                with transaction.atomic():
                    # descontar stock de productos del carrito
                    for item in carrito.items.all():
                        producto = item.producto
                        if producto.stock is not None:
                            nuevo_stock = producto.stock - item.cantidad
                            if nuevo_stock < 0:
                                nuevo_stock = 0 
                            producto.stock = nuevo_stock
                            producto.save(update_fields=['stock'])
            
            return render(request, 'confirmado.html', {'resultado': resultado})
    
    return render(request, 'fallido.html', {'resultado': resultado})

