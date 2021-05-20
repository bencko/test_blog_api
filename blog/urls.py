from django.urls import path

from .views import PostCreate, UserPostsView, FeedView, SubscribeCreateOrListView, SubscribeOperateView




urlpatterns = [
    path('', PostCreate.as_view(), name='post-create'), # tests work
    path('feed/', FeedView.as_view(), name='feed-view'),
    path('<int:pk>/posts/', UserPostsView.as_view(), name='user-posts-view'),
    path('subscribes/<int:pk>/', SubscribeOperateView.as_view(), name='subscribe-operate-view'),
    path('subscribes/', SubscribeCreateOrListView.as_view(), name='subscribe-create-or-list'),
]