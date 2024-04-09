from django.db import models
from django.urls import reverse


class Teams(models.Model):
    team_title = models.CharField(
        max_length=120,
        unique=True,
        verbose_name="Название команды"
    )

    slug = models.SlugField(
        db_index=True,
        unique=True,
        verbose_name="URL"
    )

    description = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name='Описание'
    )

    reputation = models.IntegerField(
        default=0,
        verbose_name='Репутация'
    )

    is_open = models.BooleanField(
        blank=False,
        default=True,
        null=False,
        verbose_name="Открыт набор"
    )

    def get_absolute_url(self):
        return reverse('teams:team_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'Команда {self.team_title}'

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"


class TeamMembers(models.Model):
    CREATOR = True
    MEMBER = None

    ROLES = [
        (CREATOR, 'Создатель'),
        (MEMBER, 'Член команды')
    ]

    team = models.ForeignKey(to=Teams, on_delete=models.CASCADE, related_name='team_members', verbose_name='Команда')

    user = models.ForeignKey(to='translators_hub.User', on_delete=models.CASCADE, related_name='membership')

    role = models.BooleanField(blank=True, default=None, null=True, choices=ROLES, verbose_name="Роль в команде")

    def __str__(self):
        return f'Член команды {self.team} - {self.user}, роль - {self.get_role_display()}'

    class Meta:
        verbose_name = "Член команды"
        verbose_name_plural = "Члены команды"


class TeamInvites(models.Model):
    NO_RESPONSE = 'no_resp'
    ACCEPTED = 'ok'
    DECLINED = 'no'
    STATUS = [
        (NO_RESPONSE, 'Нет ответа'),
        (ACCEPTED, 'Принято'),
        (DECLINED, 'Отклонено')
    ]

    team = models.ForeignKey(
        to=Teams,
        on_delete=models.CASCADE,
    )

    sender = models.ForeignKey(
        to='translators_hub.User',
        on_delete=models.CASCADE,
        related_name='team_sender_name'
    )

    target = models.ForeignKey(
        to='translators_hub.User',
        on_delete=models.CASCADE,
        related_name='team_target_name'
    )

    text_invite = models.CharField(
        max_length=500,
        blank=True,
    )

    status = models.CharField(
        max_length=7,
        choices=STATUS,
        blank=False,
        null=False,
        default=None,
    )

    def __str__(self):
        return f'Приглашение для {self.target}, в команду {self.team}'

    class Meta:
        verbose_name = "Приглашение"
        verbose_name_plural = "Приглашения"

