# Generated by Django 4.0.3 on 2022-04-05 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogtest', '0008_rename_comment_on_comment_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
