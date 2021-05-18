from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.authtoken.models import Token
from blog.models import Post
from datetime import datetime

# set the email field in user model unique and required
get_user_model()._meta.get_field('email')._unique = True
get_user_model()._meta.get_field('email').blank = False
get_user_model()._meta.get_field('email').null = False
# catch signal for generating auth token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_subscribes_list(sender, instance=None, created=False, **kwargs):
    if created:
        SubscribesList.objects.create(owner=instance)



def get_subs_list(self):
    my_subs_list = SubscribesList.objects.get(owner=self)
    return my_subs_list

def get_posts_from_date(self, start_date):

    today = datetime.today()
    posts = Post.objects.filter(created_at__range=[start_date, today])
    return posts

get_user_model().add_to_class("get_subs_list", get_subs_list)
get_user_model().add_to_class("get_posts_from_date", get_posts_from_date)



class Subscribe(models.Model):
    to = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    subscribed_time = models.DateTimeField(auto_now_add=True, verbose_name='subscribed_time', blank=True)
    def __str__(self):
        return 'to %s' % self.to

class SubscribesList(models.Model):
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    subscribed_to = models.ManyToManyField('Subscribe', blank=True)

    def __str__(self):
    	return 'from %s' % self.owner