from django.urls import path
from . views import *


urlpatterns = [
    path("respuesta/", webpay_respuesta, name="webpay_respuesta"),
]