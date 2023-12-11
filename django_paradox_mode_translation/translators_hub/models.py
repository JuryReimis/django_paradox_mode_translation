from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=False, unique=True, null=False)

    def __str__(self):
        return self.username


def get_image_user_path(instance, filename):
    return f'users/{instance.slug}/{filename}'


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
        upload_to=get_image_user_path,
        default='defaults/noavatar.png',
        null=False,
        verbose_name="Аватар",
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

    def get_absolute_url(self):
        return reverse('translators_hub:profile', kwargs={'slug': self.slug})

    def get_fields_in_dict(self, ):
        fields_dict = {}
        for field in self._meta.fields:
            fields_dict[field.name] = field.value_from_object(self)
        return fields_dict


def get_image_project_path(instance, filename):
    return f'translators_hub/{instance.slug}/{filename}'


class ModTranslation(models.Model):

    ENGLISH = 'en'
    FRENCH = 'fr'
    GERMAN = 'de'
    KOREAN = 'ko'
    RUSSIAN = 'ru'
    SIMPLE_CHINESE = 'zh'
    SPANISH = 'es'

    IN_WORK = 'w'
    FINISH = 'f'
    NEED_UPDATE = 'nu'

    VALID_LANGUAGES = [
        (ENGLISH, 'Английский'),
        (FRENCH, 'Французский'),
        (GERMAN, 'Немецкий'),
        (KOREAN, 'Корейский'),
        (RUSSIAN, 'Русский'),
        (SIMPLE_CHINESE, 'Китайский'),
        (SPANISH, 'Испанский')
    ]

    STATUS = [
        (IN_WORK, 'В работе'),
        (FINISH, 'Завершено'),
        (NEED_UPDATE, 'Требуется обновление')
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

    description = models.CharField(
        max_length=3000,
        null=True,
        default=None,
        verbose_name="Описание"
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
        upload_to=get_image_project_path,
        default='defaults/main icon.jpg',
        verbose_name="Обложка",
        blank=True,
        null=True
    )

    authors = models.ManyToManyField(
        to='Roles',
        blank=False,
        verbose_name="Авторы"
    )

    status = models.CharField(
        max_length=5,
        choices=STATUS,
        default=IN_WORK,
        verbose_name="Статус",
    )

    views = models.PositiveIntegerField(
        default=0,
        verbose_name="Просмотры",
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
        authors = self.authors.order_by().select_related('user__userprofile')

        order = {}
        for author in authors:
            role_name = author.get_role_display()
            order[role_name] = order.get(role_name, [])
            order[role_name].append(author.user)
        return order

    class Meta:
        verbose_name = "Перевод"
        verbose_name_plural = "Переводы"


class Roles(models.Model):
    ORGANISER = 'org'
    MODERATOR = 'mdr'
    TRANSLATOR = 'trs'
    TESTER = 'tst'
    ROLES = [
        (ORGANISER, 'Организатор'),
        (MODERATOR, 'Модератор'),
        (TRANSLATOR, 'Переводчик'),
        (TESTER, 'Тестер'),
        (None, 'Никто'),
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
        ordering = ['role']


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

    def __str__(self):
        return f'Приглашение для {self.target}, на позицию {self.get_role_display()}'

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


class AbstractComments(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posted_comments'
    )

    comment_text = models.CharField(
        max_length=1500,
        blank=False,
        default=None,
        null=False,
        verbose_name="Комментарий",
    )

    likes = models.IntegerField(
        default=0,
        blank=False,
        null=False,
    )

    dislikes = models.IntegerField(
        default=0,
        blank=False,
        null=False,
    )

    pub_date = models.DateTimeField(
        verbose_name='Дата написания комментария',
        null=True,
        auto_now_add=True,
    )

    update_date = models.DateTimeField(
        verbose_name='Дата изменения комментария',
        null=True,
        blank=True,
        auto_now=True,
    )

    visible = models.BooleanField(
        verbose_name='Отображаемый',
        default=True,
        blank=False,
        null=False,
    )

    class Meta:
        abstract = True


class ProfileComments(AbstractComments):
    author = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posted_profile_comments'
    )

    target = models.ForeignKey(
        to=UserProfile,
        on_delete=models.CASCADE,
        null=True,
        related_name='profile_comments'
    )

    def __str__(self):
        return f'Комментарий пользователя {self.author} в профиле {self.target}'

    class Meta:
        verbose_name = "Комментарий в профиле"
        verbose_name_plural = "Комментарии в профиле"


class ProjectComments(AbstractComments):
    author = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posted_project_comments'
    )

    target = models.ForeignKey(
        to=ModTranslation,
        on_delete=models.CASCADE,
        null=True,
        related_name='project_comments',
    )

    def __str__(self):
        return f'Комментарий пользователя {self.author} под проектом {self.target}'

    class Meta:
        verbose_name = "Комментарий под проектом"
        verbose_name_plural = "Комментарии под проектом"
