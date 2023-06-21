import uuid
from django.utils.crypto import get_random_string
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.db.models.signals import pre_save
# Create your models here.
class User(AbstractUser):

    username = None
    USERNAME_FIELD = 'email'
    email = models.EmailField(verbose_name='Email адрес', unique=True)
    phone = models.CharField(max_length=28, verbose_name='Номер телефона', null=True, blank=True)
    country = models.CharField(max_length=30, verbose_name='Страна', null=True, blank=True)
    avatar = models.ImageField(upload_to='users_img/', verbose_name='Аватар', null=True, blank=True)
    is_verified = models.BooleanField(default=False, verbose_name='Подтвержденный адрес')
    verif_code = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('users:confirm_email', kwargs={'slug': self.slug})


def pre_save_user_receiver(sender, instance, *args, **kwargs):
    if not instance.pk:
        # генерируем код верификации из шести случайных символов
        instance.verif_code = get_random_string(length=6)

    if not instance.slug:
        instance.slug = slugify(instance.email)

pre_save.connect(pre_save_user_receiver, sender=settings.AUTH_USER_MODEL)
