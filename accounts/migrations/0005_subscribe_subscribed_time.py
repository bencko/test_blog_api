# Generated by Django 3.2.3 on 2021-05-18 21:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210517_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribe',
            name='subscribed_time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 5, 18, 21, 36, 24, 407528), verbose_name='subscribed_time'),
            preserve_default=False,
        ),
    ]
