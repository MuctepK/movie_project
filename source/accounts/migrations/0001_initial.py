# Generated by Django 2.2.10 on 2020-03-25 08:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Профиль')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='user_images', verbose_name='Фото')),
                ('about_me', models.TextField(blank=True, max_length=1024, null=True, verbose_name='О себе')),
            ],
        ),
    ]
