from django.urls import path
from .views import getStock
from . import views

urlpatterns = [
    path('api/stock/', getStock),
    path('api/carrito/ver/', views.ver_carrito),
    path('api/carrito/agregar/', views.agregar_producto_carrito),
    path('api/carrito/ver/<str:session_key>/', views.ver_carrito_por_session),
    path('api/carrito/eliminar/<str:producto_id>/<str:session_key>/', views.eliminar_carrito)
]
