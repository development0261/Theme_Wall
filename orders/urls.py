from django.urls import path, include
from .views import *
urlpatterns = [
    path('',ordersIndex,name="ordersIndex"),
    path('cart/',cart,name="cart"),
]