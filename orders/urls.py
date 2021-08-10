from django.urls import path, include
from .views import *
urlpatterns = [
    path('',ordersIndex,name="ordersIndex"),
    path('cart/',cart,name="cart"),
    path('checkout/',checkout,name="checkout"),
    path('placeOrder/',placeOrder,name="placeOrder"),
    path('invoice/<int:id>/',invoice,name="invoice"),
    path('myOrders/',myOrders,name="myOrders"),
    path('sellerOrders/',sellerOrders,name="sellerOrders"),
    path('orderProducts/<int:id>/',orderProducts,name="orderProducts"),
    path('fetchStatus/<int:id>/',fetchStatus,name="fetchStatus"),
    path('updateStatus/',updateStatus,name="updateStatus"),
    path('addToWishList/',addToWishList,name="addToWishList"),
    path('fetchWishlist/',fetchWishlist,name="fetchWishlist"),

]