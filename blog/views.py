from rest_framework import generics, mixins
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

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

