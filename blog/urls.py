from django.urls import path

from .views import PostCreate, UserPostsView,\
    FeedView, SubscribeCreateOrListView,\
    SubscribeOperateView, ReadedPostsView

urlpatterns = [
    # tested
    path(
        '',
        PostCreate.as_view(),
        name='post-create'
    ),
    # tested generation feed
    path(
        'feed/',
        FeedView.as_view(),
        name='feed-view'
    ),
    # tested
    path(
        '<int:pk>/posts/',
        UserPostsView.as_view(),
        name='user-posts-view'
    ),
    # tested
    path(
        'subscribes/<int:pk>/',
        SubscribeOperateView.as_view(),
        name='subscribe-operate-view'
    ),
    # tested
    path(
        'subscribes/',
        SubscribeCreateOrListView.as_view(),
        name='subscribe-create-or-list'
    ),
    path(
        'readed/',
        ReadedPostsView.as_view(),
        name='mark-as-readed'
    ),
]
