from django.db import models


class Chat(models.Model):

    title = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        verbose_name="Название чата"
    )

    slug = models.SlugField(
        unique=True,
        db_index=True,
        blank=False,
        verbose_name='URL'
    )

    members = models.ManyToManyField(
        to='translators_hub.User',
        related_name='chats',
        verbose_name='Пользователи чата'
    )

    def __str__(self):
        return f'Чат {self.title}'

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"


class Message(models.Model):

    body = models.CharField(
        max_length=300,
        blank=False,
        null=False,
        verbose_name="Тело сообщения"
    )

    author = models.ForeignKey(
        to='translators_hub.User',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Автор комментария"
    )

    chat = models.ForeignKey(
        to=Chat,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name="Чат"
    )

    pub_date = models.DateTimeField(
        auto_created=True,
        verbose_name="Сообщение написано"
    )
