from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from . import serializers
from .models import Post


class PostCreate(generics.CreateAPIView):
    """
    Post creation endpoint\n
        only for authenticated users
    """
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserPostList(generics.ListAPIView):
    """
        Return post list from current user.id\n
            Example - .../api/post/from_user/1\
            - return all post of user which id=1
    """
    serializer_class = serializers.PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        qs = Post.objects.filter(owner_id=self.kwargs['pk'])
        return qs