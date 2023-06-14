from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    email = models.EmailField(unique=True, verbose_name='Email адрес')
    phone = models.CharField(max_length=28, verbose_name='Номер телефона', null=True, blank=True)
    country = models.CharField(max_length=30, verbose_name='Страна')
    avatar = models.ImageField(upload_to='users_img/', verbose_name='Аватар', null=True, blank=True)