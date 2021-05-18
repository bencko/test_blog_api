from django.urls import path

from rest_framework.authtoken import views as token_auth_views

from .views import UserCreateOrListView,\
   UserOperateView, ObtainAuthToken,\
   SubscribeCreateOrListView, SubscribeOperateView,\
   UserPostsView, FeedView




urlpatterns = [
    path('feed/', FeedView.as_view(), name='feed-view'),
    path('subscribes/<int:pk>/', SubscribeOperateView.as_view(), name='subscribe-operate-view'),
    path('subscribes/', SubscribeCreateOrListView.as_view(), name='subscribe-create-or-list'),
    path('<int:pk>/posts/', UserPostsView.as_view(), name='user-posts-view'),
    path('<int:pk>/', UserOperateView.as_view(), name='user-operate-view'),
    path('api-token-auth/', ObtainAuthToken.as_view(), name='get-token'), 
    path('', UserCreateOrListView.as_view(), name='user-create-or-list'), 
]

