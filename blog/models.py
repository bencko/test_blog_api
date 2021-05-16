from django.db import models
from django.contrib.auth import get_user_model


class Post(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length = 100, null=False, verbose_name='title')
    text = models.TextField(null=False, verbose_name='post_text')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    

    class Meta:
    	ordering = ['-created_at']

    def __str__(self):
        return str(self.title)