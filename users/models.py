from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import NULLABALE


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='почта')
    telephone = models.CharField(max_length=35, verbose_name='телефон', **NULLABALE)
    avatar = models.ImageField(upload_to='users/', **NULLABALE, verbose_name='аватар')
    country = models.CharField(max_length=150, verbose_name='страна', **NULLABALE)

    code = models.CharField(max_length=4, verbose_name='код', **NULLABALE)
    is_active = models.BooleanField(default=True, verbose_name="пользователь активен")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
