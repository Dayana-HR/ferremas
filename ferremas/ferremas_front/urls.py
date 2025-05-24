from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.vista_productos, name='index'),
    path('carrito/', views.vista_carrito_html, name='carrito')
]