from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """
    Post serializer
    """

    
    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'created_at', 'owner']
        extra_kwargs = {
            'owner': {'read_only': True}
        }

  