from django.urls import path

from rest_framework.authtoken import views as token_auth_views

from .views import UserList, UserCreate, ObtainAuthToken, redirect_to_from_max




urlpatterns = [
    path('create/', UserCreate.as_view(), name='account-create'), # tests work
    path('all/', redirect_to_from_max),
    path('all/<str:sorting>/', UserList.as_view(), name='all-users-list'), # tests work
    path('api-token-auth/', ObtainAuthToken.as_view(), name='get-token'), # tests work
]

