# Generated by Django 3.2.9 on 2021-11-30 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20211130_1007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userbase',
            name='user_name',
        ),
    ]
