from django.urls import path

from .views import PostCreate




urlpatterns = [
    path('', PostCreate.as_view(), name='post-create'), # tests work
    
]