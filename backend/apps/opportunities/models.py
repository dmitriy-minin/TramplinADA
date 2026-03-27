from django.db import models
from django.conf import settings


class Tag(models.Model):
    TAG_TYPE_SKILL = "skill"
    TAG_TYPE_LEVEL = "level"
    TAG_TYPE_EMPLOYMENT = "employment"

    TYPE_CHOICES = [
        (TAG_TYPE_SKILL, "Технология / Навык"),
        (TAG_TYPE_LEVEL, "Уровень"),
        (TAG_TYPE_EMPLOYMENT, "Тип занятости"),
    ]

    name = models.CharField("Название", max_length=100, unique=True)
    tag_type = models.CharField("Тип", max_length=20, choices=TYPE_CHOICES, default=TAG_TYPE_SKILL)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="created_tags",
    )
    is_system = models.BooleanField("Системный", default=False)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["tag_type", "name"]

    def __str__(self):
        return self.name


class Opportunity(models.Model):
    TYPE_INTERNSHIP = "internship"
    TYPE_VACANCY = "vacancy"
    TYPE_MENTORING = "mentoring"
    TYPE_EVENT = "event"

    TYPE_CHOICES = [
        (TYPE_INTERNSHIP, "Стажировка"),
        (TYPE_VACANCY, "Вакансия"),
        (TYPE_MENTORING, "Менторская программа"),
        (TYPE_EVENT, "Карьерное мероприятие"),
    ]

    FORMAT_OFFICE = "office"
    FORMAT_HYBRID = "hybrid"
    FORMAT_REMOTE = "remote"
    FORMAT_ONLINE = "online"

    FORMAT_CHOICES = [
        (FORMAT_OFFICE, "Офис"),
        (FORMAT_HYBRID, "Гибрид"),
        (FORMAT_REMOTE, "Удалённо"),
        (FORMAT_ONLINE, "Онлайн"),
    ]

    STATUS_ACTIVE = "active"
    STATUS_CLOSED = "closed"
    STATUS_PLANNED = "planned"
    STATUS_DRAFT = "draft"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Активна"),
        (STATUS_CLOSED, "Закрыта"),
        (STATUS_PLANNED, "Запланирована"),
        (STATUS_DRAFT, "Черновик"),
    ]

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="opportunities",
        verbose_name="Компания",
    )
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание")
    opp_type = models.CharField("Тип", max_length=20, choices=TYPE_CHOICES)
    work_format = models.CharField("Формат", max_length=20, choices=FORMAT_CHOICES, default=FORMAT_REMOTE)

    # Location
    address = models.CharField("Адрес", max_length=300, blank=True)
    city = models.CharField("Город", max_length=100, blank=True)
    latitude = models.DecimalField("Широта", max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField("Долгота", max_digits=9, decimal_places=6, null=True, blank=True)

    # Salary
    salary_min = models.PositiveIntegerField("Зарплата от", null=True, blank=True)
    salary_max = models.PositiveIntegerField("Зарплата до", null=True, blank=True)
    salary_currency = models.CharField("Валюта", max_length=10, default="KZT")

    # Dates
    published_at = models.DateTimeField("Дата публикации", auto_now_add=True)
    expires_at = models.DateField("Срок действия", null=True, blank=True)
    event_date = models.DateTimeField("Дата мероприятия", null=True, blank=True)

    # Status & moderation
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    is_moderated = models.BooleanField("Прошла модерацию", default=False)
    moderation_note = models.TextField("Примечание куратора", blank=True)

    # Tags
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")

    # Contact info
    contact_email = models.EmailField("Email для связи", blank=True)
    contact_phone = models.CharField("Телефон", max_length=30, blank=True)
    external_url = models.URLField("Ссылка на вакансию", blank=True)

    class Meta:
        verbose_name = "Возможность"
        verbose_name_plural = "Возможности"
        ordering = ["-published_at"]

    def __str__(self):
        return f"{self.title} — {self.company.name}"

    @property
    def salary_display(self):
        if self.salary_min and self.salary_max:
            return f"{self.salary_min:,}–{self.salary_max:,} {self.salary_currency}"
        elif self.salary_min:
            return f"от {self.salary_min:,} {self.salary_currency}"
        elif self.salary_max:
            return f"до {self.salary_max:,} {self.salary_currency}"
        return "По договорённости"

    @property
    def is_offline(self):
        return self.work_format in [self.FORMAT_OFFICE, self.FORMAT_HYBRID]

    @property
    def map_location(self):
        """Return the display location for map."""
        if self.is_offline and self.address:
            return self.address
        return self.city or (self.company.city if self.company else "")


class Application(models.Model):
    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_REJECTED = "rejected"
    STATUS_RESERVE = "reserve"

    STATUS_CHOICES = [
        (STATUS_PENDING, "На рассмотрении"),
        (STATUS_ACCEPTED, "Принят"),
        (STATUS_REJECTED, "Отклонён"),
        (STATUS_RESERVE, "В резерве"),
    ]

    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
        verbose_name="Соискатель",
    )
    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        related_name="applications",
        verbose_name="Возможность",
    )
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    cover_letter = models.TextField("Сопроводительное письмо", blank=True)
    applied_at = models.DateTimeField("Дата отклика", auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_favorite = models.BooleanField("В избранном", default=False)

    class Meta:
        verbose_name = "Отклик"
        verbose_name_plural = "Отклики"
        unique_together = [("applicant", "opportunity")]
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.applicant} → {self.opportunity.title}"
