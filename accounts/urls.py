from django.urls import path

from rest_framework.authtoken import views as token_auth_views

from .views import UserCreateOrListView, UserOperateView, ObtainAuthToken

urlpatterns = [
    path(
        '<int:pk>/',
        UserOperateView.as_view(),
        name='user-operate-view'
    ),
    # tested
    path(
        'api-token-auth/',
        ObtainAuthToken.as_view(),
        name='get-token'
    ),
    # tested
    path(
        '',
        UserCreateOrListView.as_view(),
        name='user-create-or-list'
    ),
]
