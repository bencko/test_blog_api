from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from rest_framework.response import Response
from rest_framework import generics, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken import views as auth_views
from rest_framework.authtoken.models import Token
from rest_framework import status

from blog.models import Post

from . import serializers

class ObtainAuthToken(auth_views.ObtainAuthToken):
    """
    Send to this endpoint username and password\
    and it return token for this account\n
        Add to request headers "Authorization: Token {{here_your_token}}"
        Example - "Authorization: Token 5e8fc751d300537ab11ba793edc345c890698140"
    And now you is authenticated
    """

    def get_serializer_class(self):
        return AuthTokenSerializer


class UserCreate(generics.CreateAPIView):
    """
    Creation user endpoint\n
        Need unique email, unique username and strong password
    """
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        return get_user_model().objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.get(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    """
    User list endpoint\n
    Optional parameter - {sorting}\n
    {sorting} can be "from_max" or "from_min"\n
        Example - .../api/user/all/from_max\
            - return all users ordered by total posts from max  count\n
        Example - .../api/user/all/from_min\
            - return all users ordered by total posts from min  count
    """
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        return get_user_model().objects.all()

    def get(self, request, sorting, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.serializer_class(qs, many=True)
        res = serializer.data
        res = self.sorted_serializer_data(res, sorting=sorting)
        return Response(res, status=status.HTTP_200_OK)
    
    # method for sorting serialized data
    def sorted_serializer_data(self, data, sorting='from_max'):
        if sorting == 'from_max':
            return sorted(data, key=lambda k: k['total_posts'], reverse=True)
        return sorted(data, key=lambda k: k['total_posts'])



def redirect_to_from_max(request):
    return redirect('all-users-list', sorting='from_max')