from django.contrib import admin

from .models import Post, Subscribe, SubscribesList, ReadedPostsList, ReadedPost

admin.site.register(Subscribe)
admin.site.register(SubscribesList)
admin.site.register(Post)
admin.site.register(ReadedPostsList)
admin.site.register(ReadedPost)