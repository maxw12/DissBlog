# Generated by Django 4.0.3 on 2022-04-05 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogtest', '0006_alter_comment_comment_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]