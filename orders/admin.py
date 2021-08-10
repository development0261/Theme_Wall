from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from orders.models import Order, ShippingAddress, OrderItem,wishlist

def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

class OrderAdmin(admin.ModelAdmin):

    list_filter = ['user','paymentMethod','isPaid','totalPrice','paidAt','payment_id','status']
    list_display = ['user','paymentMethod','isPaid','totalPrice','paidAt','payment_id','deliveredAt','status']
    list_editable = ['status','isPaid']

admin.site.register(Order,OrderAdmin)

class AddressAdmin(admin.ModelAdmin):

    list_filter = ['city','state',('order__id',custom_titled_filter('Order Id'))]
    list_display = ['order','address','city','state']

admin.site.register(ShippingAddress,AddressAdmin)


def custom_titled_filter(param):
    pass


class OrderItemAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src="{}" width="40" style="border-radius:50px">'.format(object.image.url))


    search_fields = ('product__title','product__pk')
    list_filter = ['product','order']
    list_display = ['product','order','name','qty','price','thumbnail']
    list_display_links = ['product','order']

admin.site.register(OrderItem,OrderItemAdmin)


admin.site.register(wishlist)