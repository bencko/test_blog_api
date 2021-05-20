from itertools import chain

from django.contrib.auth import get_user_model
from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from .models import Post, Subscribe
from .paginators import UserPostsResultsPagination

import operator

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
    #если юзать self.list() - то возвращает тупо этот сет, чтобы ты не передал в self.list()
    def get_queryset(self, *args, **kwargs):
        qs = Post.objects.none()
        try:
            user_subscriptions = self.request.user.get_subs_list()
            if user_subscriptions is not None:
                for subs in user_subscriptions.subscribed_to.all():
                    to_user = subs.to
                    created = subs.subscribed_time
                    subs_posts = to_user.get_posts_from_date(created)
                    qs = list(chain(qs, subs_posts))
                return self._sorted(qs)
        except:
            return qs
            
    def _sorted(self, data, sorting='from_max'):
        return sorted(data, key=operator.attrgetter('created_at'), reverse=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserPostsView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = serializers.PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        try:
            from_user = get_user_model().objects.get(id=self.kwargs['pk'])
            if from_user is not None:
                qs = Post.objects.filter(owner=from_user)
                return qs
        except:
            return Post.objects.none()
        
    def get(self, request, *args, **kwargs):
       return self.list(request, *args, **kwargs)


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
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
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
