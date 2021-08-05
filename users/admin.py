from django.contrib import admin
from .models import Profile,CustomeUser,SellerRequest,Address

admin.site.register(Profile)
admin.site.register(CustomeUser)
admin.site.register(SellerRequest)

class AddressModel(admin.ModelAdmin):
    list_display = ['user','city','state','pincode','country']
admin.site.register(Address,AddressModel)

