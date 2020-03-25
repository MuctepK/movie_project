from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Профиль', related_name='profile', on_delete=models.CASCADE,
                                primary_key=True)
    photo = models.ImageField(verbose_name='Фото', upload_to='user_images', null=True, blank=True)
    about_me = models.TextField(verbose_name='О себе', max_length=1024, null=True, blank=True)

