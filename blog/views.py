from django.contrib.auth import get_user_model


from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from itertools import chain

from . import serializers
from .models import Post, Subscribe
from .paginators import UserPostsResultsPagination


class PostCreate(generics.CreateAPIView):
    """
    Post creation endpoint\n
        only for authenticated users
    """
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class FeedView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserPostsResultsPagination

    def get_queryset(self, *args, **kwargs):
        return Post.objects.all()

    def get(self, request, *args, **kwargs):
        request_user_subs_list = request.user.get_subs_list()
        qs = Post.objects.none()

        for subs in request_user_subs_list.subscribed_to.all():
            to_user = subs.to
            created = subs.subscribed_time
            subs_posts = to_user.get_posts_from_date(created)
            qs = list(chain(qs, subs_posts))
        print(qs)
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserPostsView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = serializers.PostSerializer
    permission_classes = [AllowAny]
    

    def get_queryset(self):
        return get_user_model().objects.all()

    def get(self, request, *args, **kwargs):
        from_user = self.get_object()
        qs = Post.objects.filter(owner=from_user)
        serializer = self.serializer_class(qs, many=True)
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
            request_user_subs_list = request.user.get_subs_list()
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
