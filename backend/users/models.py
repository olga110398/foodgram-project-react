from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    """Модель для user."""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    username = models.CharField(
        'Username',
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(r'^[\w.@+-]+\Z'),
        ],
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
        blank=False,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        unique=True,
        blank=False,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        unique=True,
        blank=False,
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
        blank=False,
        validators=[
            RegexValidator(r'^[\w.@+-]+\Z'),
        ],
    )
    is_subscribed = models.BooleanField(default=False)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username
