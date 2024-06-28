from django.db import models
from django.urls import reverse


def get_image_project_path(instance, filename):
    return f'translators_hub/{instance.slug}/{filename}'


class Translation(models.Model):

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

    original_language = models.ForeignKey(
        to='Language',
        on_delete=models.PROTECT,
        related_name='original_language',
        verbose_name="Исходный язык"
    )

    target_language = models.ForeignKey(
        to='Language',
        on_delete=models.PROTECT,
        related_name='target_language',
        verbose_name="Целевой язык"
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
        to='auth_app.User',
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


class Language(models.Model):
    language_title = models.CharField(max_length=160, blank=False, null=False, unique=True, verbose_name="Язык")

    def __str__(self):
        return self.language_title

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"


class Invites(models.Model):

    ACCEPTED = 'ok'
    DECLINED = 'no'
    STATUS = [
        (None, 'Нет ответа'),
        (ACCEPTED, 'Принято'),
        (DECLINED, 'Отклонено')
    ]

    mod_translation = models.ForeignKey(
        to=Translation,
        on_delete=models.CASCADE,
    )

    sender = models.ForeignKey(
        to='auth_app.User',
        on_delete=models.CASCADE,
        related_name='sender_name'
    )

    target = models.ForeignKey(
        to='auth_app.User',
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

    description = models.CharField(
        max_length=1000,
        blank=True,
        null=False,
        default='',
        verbose_name="Описание"
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
        to='auth_app.User',
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


# class ProfileComments(AbstractComments):
#     author = models.ForeignKey(
#         to='auth_app.User',
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='posted_profile_comments'
#     )
#
#     target = models.ForeignKey(
#         to='auth_app.UserProfile',
#         on_delete=models.CASCADE,
#         null=True,
#         related_name='profile_comments'
#     )
#
#     def get_reactions(self) -> [int, int]:
#         likes = 0
#         dislikes = 0
#         for reaction in self.profile_comment_reactions.all():
#             if reaction.reaction is True:
#                 likes += 1
#             elif reaction.reaction is False:
#                 dislikes += 1
#         return likes, dislikes
#
#     def __str__(self):
#         return f'Комментарий пользователя {self.author} в профиле {self.target}'
#
#     class Meta:
#         verbose_name = "Комментарий в профиле"
#         verbose_name_plural = "Комментарии в профиле"


# class ProfileCommentsReaction(models.Model):
#     LIKE = True
#     DISLIKE = False
#
#     REACTION = [
#         (LIKE, "Лайк"),
#         (DISLIKE, "Дизлайк"),
#         (None, "Нет реакции"),
#     ]
#
#     author = models.ForeignKey(
#         to='auth_app.User',
#         on_delete=models.SET_NULL,
#         null=True,
#         verbose_name='Автор реакции'
#     )
#
#     target = models.ForeignKey(
#         to=ProfileComments,
#         on_delete=models.CASCADE,
#         related_name='profile_comment_reactions',
#         verbose_name='Комментарий'
#     )
#
#     reaction = models.BooleanField(
#         choices=REACTION,
#         null=True,
#         blank=True,
#         verbose_name='Реакция на комментарий'
#     )
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['author', 'target'], name='unique_profile_comment_reaction')
#         ]
#         verbose_name = "Реакция на комментарий"
#         verbose_name_plural = "Реакции на комментарии"


# class ProjectComments(AbstractComments):
#     author = models.ForeignKey(
#         to='auth_app.User',
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='posted_project_comments'
#     )
#
#     target = models.ForeignKey(
#         to=Translation,
#         on_delete=models.CASCADE,
#         null=True,
#         related_name='project_comments',
#     )
#
#     def get_reactions(self) -> [int, int]:
#         likes = 0
#         dislikes = 0
#         for reaction in self.project_comment_reactions.all():
#             if reaction.reaction is True:
#                 likes += 1
#             elif reaction.reaction is False:
#                 dislikes += 1
#         return likes, dislikes
#
#     def __str__(self):
#         return f'Комментарий пользователя {self.author} под проектом {self.target}'
#
#     class Meta:
#         verbose_name = "Комментарий под проектом"
#         verbose_name_plural = "Комментарии под проектом"


# class ProjectCommentsReaction(models.Model):
#     LIKE = True
#     DISLIKE = False
#
#     REACTION = [
#         (LIKE, "Лайк"),
#         (DISLIKE, "Дизлайк"),
#         (None, "Нет реакции"),
#     ]
#
#     author = models.ForeignKey(
#         to='auth_app.User',
#         on_delete=models.SET_NULL,
#         null=True,
#         verbose_name='Автор реакции'
#     )
#
#     target = models.ForeignKey(
#         to=ProjectComments,
#         on_delete=models.CASCADE,
#         related_name='project_comment_reactions',
#         verbose_name='Комментарий'
#     )
#
#     reaction = models.BooleanField(
#         choices=REACTION,
#         null=True,
#         blank=True,
#         verbose_name='Реакция на комментарий'
#     )
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['author', 'target'], name='unique_project_comment_reaction')
#         ]
