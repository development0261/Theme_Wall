from django.urls import path, include
from .views import *
urlpatterns = [
    path("",allProducts,name="allProducts"),
    path("sellerDash/",sellerDash,name="sellerDash"),
    path("addCategory/",addCategory,name="addCategory"),
    path("addProduct/",addProduct,name="addProduct"),
    path("deleteProduct/<int:id>/",deleteProduct,name="deleteProduct"),
    path("buyproducts/",buyproducts,name="buyproducts"),
    path("profile/",profile,name="profile"),
    path("buyerprofile/",buyerprofile,name="buyerprofile"),
    path("getProduct/<int:id>/",getProduct,name="getProduct"),
    path("updateProduct/<int:id>/",updateProduct,name="updateProduct"),
    path("buyproducts/",buyproducts,name="buyproducts"),
    path("checkwebcam/",checkwebcam,name="checkwebcam"),
    path("singleProduct/<int:id>/",singleProduct,name="singleProduct"),
    path("addExtraImage/<int:id>/",addExtraImage,name="addExtraImage"),
    path("getExtraImages/<int:id>/",getExtraImages,name="getExtraImages"),
    path("removeExtraImage/<int:id>/",removeExtraImage,name="removeExtraImage"),
    path("getColorBySize/<str:size>/<int:id>/",getColorBySize,name="getColorBySize"),
    path("getImageBySizeandColor/<int:id>/<str:size>/<str:color>/",getImageBySizeandColor,name="getImageBySizeandColor"),
    path("getImageById/<int:id>/",getImageById,name="getImageById")
]