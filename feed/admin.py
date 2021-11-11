from django.contrib import admin
from .models import Messages, Post, Comments, Like, Notification

admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Like)
admin.site.register(Notification)
admin.site.register(Messages)

