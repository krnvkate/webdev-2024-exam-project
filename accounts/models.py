from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='users_avatar', blank=True, verbose_name="Фото профиля")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    country = models.CharField(max_length=50, null=True, blank=True, verbose_name="Страна")
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name="Город")
    info = models.TextField(null=True, blank=True, verbose_name="О себе")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
