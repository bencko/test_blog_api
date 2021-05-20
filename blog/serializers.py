from rest_framework import serializers

from .models import Post, Subscribe, ReadedPost



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

  

class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ['id', 'to']


class ReadedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadedPost
        fields = ['id', 'post', 'readed_time']
