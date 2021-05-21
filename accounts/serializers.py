from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from blog.models import Post


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer
    """
    total_posts = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'total_posts' ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    # for validation posted password - if it strong
    def validate_password(self, value):
        validate_password(value)
        return value
    
    # method for SerializerMethodField
    # return user total posts
    def get_total_posts(self, user):
        return Post.objects.filter(owner_id=user.id).count()


    