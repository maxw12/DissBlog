# Generated by Django 4.0.3 on 2022-04-05 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogtest', '0004_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='comment_by',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='submission',
            new_name='comment_on',
        ),
    ]
