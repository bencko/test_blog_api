from django.urls import path

from .views import PostCreate, UserPostList




urlpatterns = [
    path('create/', PostCreate.as_view(), name='post-create'), # tests work
    path('from_user/<int:pk>/', UserPostList.as_view(), name='user-posts'), # tests work
    
]