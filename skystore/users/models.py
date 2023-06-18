import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):

    username = None
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True, verbose_name='Email адрес')
    phone = models.CharField(max_length=28, verbose_name='Номер телефона', null=True, blank=True)
    country = models.CharField(max_length=30, verbose_name='Страна')
    avatar = models.ImageField(upload_to='users_img/', verbose_name='Аватар', null=True, blank=True)
    is_verified = models.BooleanField(default=False, verbose_name='Подтвержденный адрес')
    verif_code = models.CharField(max_length=255, blank=True, null=True)

    def key_gen(self):
        return str(uuid.uuid4())