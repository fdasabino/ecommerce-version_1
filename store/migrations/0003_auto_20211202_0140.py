# Generated by Django 3.2.9 on 2021-12-02 00:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0002_product_users_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='users_wishlist',
        ),
        migrations.AddField(
            model_name='product',
            name='users_saved_items',
            field=models.ManyToManyField(blank=True, related_name='saved_items', to=settings.AUTH_USER_MODEL),
        ),
    ]
