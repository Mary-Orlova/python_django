"""
Модель Профиль пользователей + путь-герации для аватарки.
"""


from django.db import models
from django.contrib.auth.models import User


def avatar_path(instance: 'Profile', filename: str) -> str:
    return 'profile/avatar_profile{pk}/{filename}'.format(
        pk=instance.pk,
        filename=filename,
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(blank=True, null=True, upload_to=avatar_path)
