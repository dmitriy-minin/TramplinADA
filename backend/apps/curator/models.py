from django.db import models
from django.conf import settings


class CuratorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="curator_profile",
    )
    university = models.CharField("Вуз / Организация", max_length=200, blank=True)
    position = models.CharField("Должность", max_length=200, blank=True)
    is_admin = models.BooleanField("Администратор", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Профиль куратора"
        verbose_name_plural = "Профили кураторов"

    def __str__(self):
        return f"Куратор: {self.user}"
