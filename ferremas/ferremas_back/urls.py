from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProductoViewSet


urlpatterns = [
    path('api/stock/<int:id>', views.getStock, name='get-stock'),
    path('api/carrito/ver/', views.ver_carrito, name='vercarrito'),
    path('api/carrito/agregar/', views.agregar_producto_carrito),
    path('api/carrito/ver/<str:session_key>/', views.ver_carrito_por_session),
    path('api/carrito/eliminar/<str:producto_id>/<str:session_key>/', views.eliminar_carrito),
    path('api/carrito/pagar/', views.pagar_carrito),
    
]

# las rutas de los ViewSets
router = DefaultRouter()
router.register('categorias', CategoriaViewSet)
router.register('productos', ProductoViewSet)

urlpatterns += router.urls
