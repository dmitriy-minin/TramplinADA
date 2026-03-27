from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_APPLICANT = "applicant"
    ROLE_EMPLOYER = "employer"
    ROLE_CURATOR = "curator"

    ROLE_CHOICES = [
        (ROLE_APPLICANT, "Соискатель"),
        (ROLE_EMPLOYER, "Работодатель"),
        (ROLE_CURATOR, "Куратор"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_APPLICANT)
    display_name = models.CharField("Отображаемое имя", max_length=150, blank=True)

    # Applicant fields
    full_name = models.CharField("ФИО", max_length=200, blank=True)
    university = models.CharField("Вуз", max_length=200, blank=True)
    graduation_year = models.PositiveIntegerField("Год выпуска / Курс", null=True, blank=True)
    bio = models.TextField("О себе", blank=True)
    skills = models.TextField("Навыки (через запятую)", blank=True)
    experience = models.TextField("Опыт / Проекты", blank=True)
    github_url = models.URLField("GitHub", blank=True)
    portfolio_url = models.URLField("Портфолио", blank=True)
    resume_url = models.URLField("Резюме (ссылка)", blank=True)

    # Privacy
    profile_public = models.BooleanField("Профиль открыт всем", default=False)
    hide_applications = models.BooleanField("Скрыть отклики", default=False)

    # Contacts (friends/network)
    contacts = models.ManyToManyField(
        "self",
        symmetrical=True,
        blank=True,
        verbose_name="Контакты",
    )

    # Contact requests (one-directional until accepted)
    contact_requests = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="pending_requests",
        verbose_name="Входящие заявки",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.display_name or self.username

    @property
    def is_applicant(self):
        return self.role == self.ROLE_APPLICANT

    @property
    def is_employer(self):
        return self.role == self.ROLE_EMPLOYER

    @property
    def is_curator(self):
        return self.role == self.ROLE_CURATOR
