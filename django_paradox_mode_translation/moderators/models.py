from django.db import models


class Query(models.Model):

    NO_MODERATOR = None
    IN_WORK = 'w'
    COMPLETE = 'c'
    DENIED = 'd'

    STATUS = [
        (NO_MODERATOR, "Нет исполнителя"),
        (IN_WORK, "В работе"),
        (COMPLETE, "Выполнено"),
        (DENIED, "В запросе отказано")
    ]

    query_text = models.CharField(
        max_length=4500,
        blank=False,
        null=False,
        verbose_name="Текст заявки"
    )

    topic = models.ForeignKey(
        to='Topic',
        on_delete=models.PROTECT,
        related_name='topic_queries'
    )

    query_author = models.ForeignKey(
        to='translators_hub.User',
        on_delete=models.SET_NULL,
        related_name="user_queries",
        default=None,
        null=True,
        verbose_name="Автор заявки"
    )

    pub_date = models.DateTimeField(
        verbose_name="Заявка опубликована",
        null=False,
        auto_now_add=True
    )

    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default=None,
        null=True,
        verbose_name="Статус заявки"
    )

    query_considered = models.ForeignKey(
        to='translators_hub.User',
        on_delete=models.SET_NULL,
        related_name='queries_in_work',
        null=True,
        default=None,
        verbose_name="Модератор, принявший заявку"
    )

    denial_reason = models.CharField(
        max_length=1000,
        blank=False,
        default=None,
        null=True,
        verbose_name="Причина отказа"
    )

    accept_date = models.DateTimeField(
        verbose_name="Заявка принята к рассмотрению",
        default=None,
        null=True,
    )

    complete_date = models.DateTimeField(
        verbose_name="Заявка рассмотрена",
        default=None,
        null=True,
    )

    def __str__(self):
        return f'Заявка №{self.pk}'

    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"


class Topic(models.Model):

    topic_title = models.CharField(
        max_length=120,
        blank=False,
        unique=True,
        verbose_name="Тема обращения"
    )

    def __str__(self):
        return f'Тема - {self.topic_title}'

    class Meta:
        verbose_name = "Тема обращения"
        verbose_name_plural = "Темы обращений"
