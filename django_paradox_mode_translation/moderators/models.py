from django.db import models


class Query(models.Model):

    query_text = models.CharField(
        max_length=4500,
        blank=False,
        null=False,
        verbose_name="Текст заявки"
    )

    topic_of_query = models.ForeignKey(
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

    status = models.ForeignKey(
        to='Status',
        on_delete=models.PROTECT,
        related_name='status_queries',
        verbose_name="Статус заявки",
    )

    query_considered = models.ForeignKey(
        to='translators_hub.User',
        on_delete=models.SET_NULL,
        related_name='queries_in_work',
        null=True,
        default=None,
        verbose_name="Модератор, принявший заявку"
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


class Topic(models.Model):

    pass


class Status(models.Model):

    pass
