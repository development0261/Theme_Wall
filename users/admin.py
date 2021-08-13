from django.contrib import admin
from .models import Profile,CustomeUser,SellerRequest,Address,Messages

admin.site.register(Profile)
admin.site.register(CustomeUser)
admin.site.register(SellerRequest)

class AddressModel(admin.ModelAdmin):
    list_display = ['user','city','state','pincode','country']
admin.site.register(Address,AddressModel)


class MessageAdmin(admin.ModelAdmin):
    list_display = ['email','firstname','lastname','content']
    list_display_links = ['email']
    list_filter = ['email']
admin.site.register(Messages,MessageAdmin)