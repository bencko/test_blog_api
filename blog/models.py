from django.db import models
from django.contrib.auth import get_user_model


class Post(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False, verbose_name='title')
    text = models.TextField(null=False, verbose_name='post_text')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='created_at'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.title)


class Subscribe(models.Model):
    to = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    subscribed_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='subscribed_time',
        blank=True
    )

    def __str__(self):
        return 'to %s' % self.to


class SubscribesList(models.Model):
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    subscribed_to = models.ManyToManyField('Subscribe', blank=True)

    def __str__(self):
        return 'from %s' % self.owner


class ReadedPostsList(models.Model):
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    were_read = models.ManyToManyField('ReadedPost', blank=True)

    def __str__(self):
        return 'Readed by %s' % self.owner


class ReadedPost(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    readed_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='subscribed_time',
        blank=True
    )

    def __str__(self):
        return 'Readed post - %s' % self.post
