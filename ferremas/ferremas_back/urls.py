from django.urls import path
from .views import getStock

urlpatterns = [
    path('api/stock/', getStock),
]
