from django.contrib.auth.models import AbstractUser
from django.db import models

from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=False, unique=True, null=False)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return self.userprofile.get_absolute_url()


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
        to='translators_hub.Titles',
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