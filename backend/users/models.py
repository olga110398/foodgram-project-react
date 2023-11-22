from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
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
            UnicodeUsernameValidator(),
        ],
    )
    email = models.EmailField(
        'Адрес электронной почты',
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        unique=True,
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
        null=False,
        validators=[
            RegexValidator(r'^[\w.@+-]+\Z'),
        ],
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username
