from django.db import models
from slugify import slugify


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

    def get_chat_type(self):
        return self.CHAT_TYPE


class PrivateChat(Chat):

    CHAT_TYPE = 'private'

    members = models.ManyToManyField(
        to='translators_hub.User',
        related_name='private_chats',
        verbose_name='Пользователи чата'
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Личный чат"
        verbose_name_plural = "Личные чаты"


class TeamChat(Chat):

    team = models.OneToOneField(
        to='teams.Teams',
        on_delete=models.CASCADE,
        null=False,
        related_name='team_chat',
        verbose_name="Команда"
    )

    @classmethod
    def get_chat_params(cls, team_title: str):
        default_name = "Чат команды"
        chat_title = f'{default_name} {team_title}'
        chat_slug = slugify(chat_title)
        return {'title': chat_title, 'slug': chat_slug}

    def __str__(self):
        return f'Чат команды {self.team.team_title}'

    class Meta:
        verbose_name = "Командный чат"
        verbose_name_plural = "Командные чаты"


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

    pub_date = models.DateTimeField(
        auto_created=True,
        verbose_name="Сообщение написано"
    )

    class Meta:
        abstract = True


class PrivateMessage(Message):
    chat = models.ForeignKey(
        to=PrivateChat,
        on_delete=models.CASCADE,
        related_name='private_messages',
        verbose_name="Чат"
    )

    def __str__(self):
        return f'Личное сообщение {self.author} в чате {self.chat}'

    class Meta:
        verbose_name = "Личное сообщение"
        verbose_name_plural = "Личные сообщения"


class TeamMessage(Message):
    chat = models.ForeignKey(
        to=TeamChat,
        on_delete=models.CASCADE,
        related_name='team_messages',
        verbose_name="Командный чат"
    )

    def __str__(self):
        return f'Сообщение от {self.author} в чат команды'

    class Meta:
        verbose_name = "Сообщение в чат команды"
        verbose_name_plural = "Сообщения в чат команды"
