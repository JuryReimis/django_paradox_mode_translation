import django.contrib.auth.models
from django.db import models


class ModTranslation(models.Model):
    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название',
    )

    mode_name = models.CharField(
        max_length=100,
        blank=False,
        unique=True,
        verbose_name='Перевод для модификации:'
    )

    steam_link = models.URLField(
        max_length=200,
        blank=True,
        verbose_name='Ссылка на мастерскую'
    )

    paradox_plaza_link = models.URLField(
        max_length=200,
        blank=True,
        verbose_name='Ссылка на Плазу'
    )

    image = models.ImageField(
        verbose_name='Иллюстрация'
    )

    authors = models.ManyToManyField(
        to=django.contrib.auth.models.User
    )

    views = models.PositiveIntegerField(
        default=0
    )
