from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.authtoken.models import Token
from blog.models import Post, SubscribesList, ReadedPostsList
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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_readed_posts_list(sender, instance=None, created=False, **kwargs):
    if created:
        ReadedPostsList.objects.create(owner=instance)


def get_subs_list(self):
    my_subs_list = SubscribesList.objects.get(owner=self)
    return my_subs_list


def get_posts_from_date(self, start_date):
    today = datetime.today()
    posts = Post.objects.filter(
        owner=self,
        created_at__range=[start_date, today]
    )
    return posts


def check_in_readed_posts(self, data):
    my_r_list = ReadedPostsList.objects.get(owner=self)
    post_id = data.get('post', None)
    if post_id is not None:
        try:
            res = my_r_list.were_read.all().get(post_id=post_id)
            return True
        except Exception as e:
            print(e)
    return False


def check_in_feed(self, data):
    try:
        my_subs_list = SubscribesList.objects.get(owner=self)
        post = Post.objects.get(id=data.get('post', None))
        post_autor = get_user_model().objects.get(post=post)
        subscribe = my_subs_list.subscribed_to.get(to=post_autor)
        if post.created_at > subscribe.subscribed_time:
            return True
        return False
    except:
        return False


get_user_model().add_to_class("get_subs_list", get_subs_list)
get_user_model().add_to_class("get_posts_from_date", get_posts_from_date)
get_user_model().add_to_class("check_in_readed_posts", check_in_readed_posts)
get_user_model().add_to_class("check_in_feed", check_in_feed)
