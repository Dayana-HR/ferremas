from django.urls import path
from . import views


urlpatterns = [
    path('', views.vista_productos, name='index'),
    path('carrito/', views.vista_carrito_html, name='carrito'),
    path('estado-confirmado/', views.pago_confirmado, name='estado-confirmado')
]