# Generated by Django 4.0.4 on 2022-05-25 15:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_article_publish_alter_article_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
