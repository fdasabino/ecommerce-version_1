# Generated by Django 3.2.9 on 2021-11-30 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userbase',
            old_name='first_name',
            new_name='full_name',
        ),
    ]