from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from rest_framework.response import Response
from rest_framework import generics, views
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken import views as auth_views
from rest_framework.authtoken.models import Token
from rest_framework import status

from blog.models import Post

from . import serializers
from .models import SubscribesList, Subscribe
from blog.serializers import PostSerializer
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


class UserCreateOrListView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """
    Creation and list  user endpoint\n
        If create - need unique email, unique username and strong password
        If get list - need get parameter "sorting"\n
        ex. - .../users?sorting=from_min\n
        ex. - .../users?sorting=from_max
        \n
        Default sorting - from_max
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

    def get(self, request,  *args, **kwargs):
        sorting = request.GET.get('sorting', 'from_max')
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


class UserOperateView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]
    queryset = get_user_model().objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UserPostsView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return get_user_model().objects.all()

    def get(self, request, *args, **kwargs):
        from_user = self.get_object()
        qs = Post.objects.filter(owner=from_user)
        serializer = PostSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscribeCreateOrListView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    serializer_class = serializers.SubscribeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscribe.objects.filter(subscribeslist__owner = self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            request_user_subs_list = SubscribesList.objects.get(owner=request.user)
            subscribed = False
            try:
                if request_user_subs_list.subscribed_to.all().get(to=request.POST.get('to')):
                    subscribed = True
                    return Response({'detail' : 'You already subscribe to this user'}, status=status.HTTP_201_CREATED)
            except:
                if not subscribed:
                    subscribe = serializer.save()
                    request_user_subs_list.subscribed_to.add(subscribe)
                    request_user_subs_list.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SubscribeOperateView(generics.GenericAPIView, mixins.DestroyModelMixin):
    serializer_class = serializers.SubscribeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscribe.objects.filter(subscribeslist__owner = self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)




