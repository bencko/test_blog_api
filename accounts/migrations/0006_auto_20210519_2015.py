# Generated by Django 3.2.3 on 2021-05-19 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_subscribe_subscribed_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscribeslist',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='subscribeslist',
            name='subscribed_to',
        ),
        migrations.DeleteModel(
            name='Subscribe',
        ),
        migrations.DeleteModel(
            name='SubscribesList',
        ),
    ]
