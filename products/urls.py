from django.urls import path, include
from .views import allProducts,sellerDash,addCategory,addProduct,deleteProduct,buyproducts,profile,getProduct
urlpatterns = [
    path("",allProducts,name="allProducts"),
    path("sellerDash/",sellerDash,name="sellerDash"),
    path("addCategory/",addCategory,name="addCategory"),
    path("addProduct/",addProduct,name="addProduct"),
    path("deleteProduct/<int:id>/",deleteProduct,name="deleteProduct"),
    path("buyproducts/",buyproducts,name="buyproducts"),
    path("profile/",profile,name="profile"),
    path("getProduct/<int:id>/",getProduct,name="getProduct"),
]