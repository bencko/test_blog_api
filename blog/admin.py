from django.contrib import admin

from .models import Post, Subscribe, SubscribesList

admin.site.register(Subscribe)
admin.site.register(SubscribesList)
admin.site.register(Post)