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

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_subscribes_list(sender, instance=None, created=False, **kwargs):
    if created:
        SubscribesList.objects.create(owner=instance)


class Subscribe(models.Model):
    to = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    
    def __str__(self):
        return 'to %s' % self.to

class SubscribesList(models.Model):
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    subscribed_to = models.ManyToManyField('Subscribe', blank=True)

    def __str__(self):
    	return 'from %s' % self.owner