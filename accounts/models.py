from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token

# set the email field in user model unique and required
get_user_model()._meta.get_field('email')._unique = True
get_user_model()._meta.get_field('email').blank = False
get_user_model()._meta.get_field('email').null = False

# catch signal for generating auth token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)