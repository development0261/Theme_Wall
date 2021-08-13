from django.contrib import admin
from django.utils.html import format_html

from .models import *
# Register your models here.

class SizeInliner(admin.TabularInline):
    model = item_size
    extra = 0

class colorInliner(admin.TabularInline):
    model = item_color
    extra = 0

class SizeAdmin(admin.ModelAdmin):
    list_display = ['size','item']

admin.site.register(item_size,SizeAdmin)


class ColorAdmin(admin.ModelAdmin):
    list_display = ['color','item']

admin.site.register(item_color,ColorAdmin)

class QtyAdmin(admin.ModelAdmin):
    list_display = [
      'product','quantity','size','color'
    ]
    list_editable = ['quantity']
admin.site.register(item_qty,QtyAdmin)

class itemAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src="{}" width="40" style="border-radius:50px">'.format(object.image.url))
    list_display = ['id','name','price','is_available','thumbnail']
    inlines = (SizeInliner,colorInliner)


    list_display_links = ['name','id']

admin.site.register(item,itemAdmin)

class categoryAdmin(admin.ModelAdmin):
    list_display_links = ['name', 'id']
    list_display = ['name', 'id']

admin.site.register(category,categoryAdmin)