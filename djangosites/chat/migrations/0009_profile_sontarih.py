# Generated by Django 3.1.6 on 2021-06-06 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='sontarih',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
