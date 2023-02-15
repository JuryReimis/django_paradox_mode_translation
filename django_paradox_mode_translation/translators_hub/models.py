import django.contrib.auth.models
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=False, unique=True, null=False)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('translators_hub:profile', kwargs={'slug': self.userprofile.slug})


class UserProfile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
    )

    slug = models.SlugField(
        blank=False,
        db_index=True,
        unique=True,
        verbose_name="URL"
    )

    titles = models.ManyToManyField(
        to='Titles',
        blank=True,
        verbose_name="Награды",
    )

    description = models.TextField(
        blank=True,
        default="",
        null=True,
        verbose_name="Немного о себе",
    )

    experience = models.TextField(
        null=True,
        default="",
        verbose_name="Опыт"
    )

    profile_image = models.ImageField(
        blank=True,
        null=True,
        verbose_name="Аватар"
    )

    reputation = models.IntegerField(
        default=0,
        blank=False,
        verbose_name="Репутация",
    )

    def __str__(self):
        return f"Профиль {self.user}"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def get_fields_in_dict(self, ):
        fields_dict = {}
        for field in self._meta.fields:
            fields_dict[field.name] = field.value_from_object(self)
        return fields_dict


class ModTranslation(models.Model):

    ENGLISH = 'en'
    FRENCH = 'fr'
    GERMAN = 'de'
    KOREAN = 'ko'
    RUSSIAN = 'ru'
    SIMPLE_CHINESE = 'zh'
    SPANISH = 'es'

    VALID_LANGUAGES = [
        (ENGLISH, 'Английский'),
        (FRENCH, 'Французский'),
        (GERMAN, 'Немецкий'),
        (KOREAN, 'Корейский'),
        (RUSSIAN, 'Русский'),
        (SIMPLE_CHINESE, 'Китайский'),
        (SPANISH, 'Испанский')
    ]

    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название",
    )

    slug = models.SlugField(
        db_index=True,
        unique=True,
        verbose_name="URL",
    )

    mode_name = models.CharField(
        max_length=100,
        blank=False,
        unique=True,
        verbose_name="Перевод для модификации:"
    )

    game = models.ForeignKey(
        to='Game',
        on_delete=models.CASCADE,
        default=None,
        blank=True
    )

    original_language = models.CharField(
        max_length=5,
        choices=VALID_LANGUAGES,
        blank=False,
        default=ENGLISH
    )

    target_language = models.CharField(
        max_length=5,
        choices=VALID_LANGUAGES,
        blank=False,
        default=RUSSIAN
    )

    steam_link = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        unique=True,
        default=None,
        verbose_name="Ссылка на мастерскую"
    )

    paradox_plaza_link = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        unique=True,
        default=None,
        verbose_name="Ссылка на Плазу"
    )

    image = models.ImageField(
        verbose_name="Иллюстрация",
        blank=True,
        null=True
    )

    authors = models.ManyToManyField(
        to='Roles',
        blank=False,
        verbose_name="Авторы"
    )

    views = models.PositiveIntegerField(
        default=0
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    def get_absolute_url(self):
        return reverse('translators_hub:detail_page', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def get_sorted_roles(self):
        authors = self.authors.order_by('role')

        order = {}
        for author in authors:
            role_name = Invites.get_role_name(author.role)
            order[role_name] = order.get(role_name, [])
            order[role_name].append(author.user)
        return order

    def get_user_role(self, user: User):
        author = self.authors.get(user=user)
        role = author.role
        return role

    class Meta:
        verbose_name = "Перевод"
        verbose_name_plural = "Переводы"


class Roles(models.Model):
    ORGANISER = 'org'
    MODERATOR = 'mdr'
    TRANSLATOR = 'trs'
    TESTER = 'tst'
    ROLES = [
        (None, 'Никто'),
        (ORGANISER, 'Организатор'),
        (MODERATOR, 'Модератор'),
        (TRANSLATOR, 'Переводчик'),
        (TESTER, 'Тестер'),
    ]

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        blank=True,
        related_name='roles',
        verbose_name='Пользователь',
    )

    role = models.CharField(
        max_length=5,
        choices=ROLES,
        blank=True,
        default=None,
        null=True,
    )

    def __str__(self):
        return f'{self.user} с ролью - {self.get_role_display()}'


    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"


class Invites(models.Model):

    ACCEPTED = 'ok'
    DECLINED = 'no'
    STATUS = [
        (None, 'Нет ответа'),
        (ACCEPTED, 'Принято'),
        (DECLINED, 'Отклонено')
    ]

    mod_translation = models.ForeignKey(
        to=ModTranslation,
        on_delete=models.CASCADE,
    )

    sender = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='sender_name'
    )

    target = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='target_name'
    )

    role = models.CharField(
        max_length=5,
        choices=Roles.ROLES,
        default=None,
        null=True
    )

    text_invite = models.CharField(
        max_length=500,
        blank=True,
    )

    status = models.CharField(
        max_length=2,
        choices=STATUS,
        blank=True,
        null=True,
        default=None,
    )

    @classmethod
    def get_role_name(cls, role):
        role = Invites(role=role)
        return role.get_role_display()

    def __str__(self):
        return f'Приглашение для {self.target}, на позицию {self.get_role_name(self.role)}'

    class Meta:
        verbose_name = "Приглашение"
        verbose_name_plural = "Приглашения"


class Game(models.Model):
    game_name = models.CharField(
        max_length=60,
        blank=False,
        null=False
    )

    def __str__(self):
        return self.game_name

    class Meta:
        verbose_name = "Игры"
        verbose_name_plural = "Игры"


class Titles(models.Model):
    title = models.CharField(
        max_length=60,
        blank=False,
        null=False,
    )

    description = models.TextField(
        blank=False,
        help_text="Описание звания",
        null=False,
    )

    class Meta:
        verbose_name = "Титул"
        verbose_name_plural = "Титулы"


class ProfileComments(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='comments'
    )

    target = models.ForeignKey(
        to=UserProfile,
        on_delete=models.CASCADE,
        null=True,
        related_name='comments_targets'
    )

    comment_text = models.CharField(
        max_length=1500,
        blank=False,
        default=None,
        null=False,
        verbose_name="Комментарий",
    )

    pub_date = models.DateTimeField(
        verbose_name='Дата написания комментария',
        null=True,
    )

    update_date = models.DateTimeField(
        verbose_name='Дата изменения комментария',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Комментарий пользователя {self.author}'

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
