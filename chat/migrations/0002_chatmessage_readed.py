# Generated by Django 4.0 on 2022-08-29 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='readed',
            field=models.BooleanField(default=False),
        ),
    ]
