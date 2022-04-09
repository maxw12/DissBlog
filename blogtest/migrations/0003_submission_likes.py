# Generated by Django 4.0.3 on 2022-04-02 16:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogtest', '0002_remove_course_course_course_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='likes',
            field=models.ManyToManyField(related_name='blog_submission', to=settings.AUTH_USER_MODEL),
        ),
    ]