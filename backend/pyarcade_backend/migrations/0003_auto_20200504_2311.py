# Generated by Django 3.0.5 on 2020-05-04 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyarcade_backend', '0002_auto_20200504_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendshipmodel',
            name='user_one',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='friendshipmodel',
            name='user_two',
            field=models.CharField(max_length=30),
        ),
    ]
