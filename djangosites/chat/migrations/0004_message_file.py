# Generated by Django 3.1.6 on 2021-05-18 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_message_what_is_it'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='file',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]