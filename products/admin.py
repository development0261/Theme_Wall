from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import *
# Register your models here.

class SizeInliner(admin.TabularInline):
    model = item_size
    extra = 0

class colorInliner(admin.TabularInline):
    model = item_color
    extra = 0

class SizeAdmin(admin.ModelAdmin):
    list_display = ['id','size','item']

admin.site.register(item_size,SizeAdmin)


class ColorAdmin(admin.ModelAdmin):
    list_display = ['id','color','item']

admin.site.register(item_color,ColorAdmin)

class QtyAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius:50px">'.format(object.image.image.url))
    list_display = [
      'product','quantity','size','color','thumbnail'
    ]
    list_editable = ['quantity']
admin.site.register(item_qty,QtyAdmin)

class extraImageAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src="{}" width="40" style="border-radius:50px">'.format(object.image.url))
    list_display = ['id','product','size','color','thumbnail']

admin.site.register(Images,extraImageAdmin)

class extraImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        # ex. the name of column is "image"
        if obj.image:
            return mark_safe(
                '<img src="{0}" width="100" height="100" style="object-fit:contain" />'.format(obj.image.url))
        else:
            return '(No image)'

    image_preview.short_description = 'Preview'
    extra = 0




class itemAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src="{}" width="40" style="border-radius:50px">'.format(object.image.url))
    list_display = ['id','name','price','is_available','thumbnail']
    inlines = (extraImageInline,SizeInliner,colorInliner)


    list_display_links = ['name','id']

admin.site.register(item,itemAdmin)

class categoryAdmin(admin.ModelAdmin):
    list_display_links = ['name', 'id']
    list_display = ['name', 'id']

admin.site.register(category,categoryAdmin)

