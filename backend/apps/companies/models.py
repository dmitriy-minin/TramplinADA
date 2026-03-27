from django.db import models
from django.conf import settings


class Company(models.Model):
    INDUSTRY_CHOICES = [
        ("it", "IT / Разработка"),
        ("fintech", "Финтех"),
        ("ecommerce", "E-commerce"),
        ("telecom", "Телеком"),
        ("education", "Образование"),
        ("healthcare", "Здравоохранение"),
        ("consulting", "Консалтинг"),
        ("media", "Медиа / Реклама"),
        ("other", "Другое"),
    ]

    STATUS_PENDING = "pending"
    STATUS_VERIFIED = "verified"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "На проверке"),
        (STATUS_VERIFIED, "Верифицирована"),
        (STATUS_REJECTED, "Отклонена"),
    ]

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company",
        verbose_name="Владелец",
    )
    name = models.CharField("Название компании", max_length=200)
    description = models.TextField("Описание", blank=True)
    industry = models.CharField("Отрасль", max_length=50, choices=INDUSTRY_CHOICES, default="it")
    website = models.URLField("Сайт", blank=True)
    linkedin = models.URLField("LinkedIn", blank=True)
    telegram = models.URLField("Telegram", blank=True)
    hh_url = models.URLField("HeadHunter", blank=True)
    logo = models.ImageField("Логотип", upload_to="company_logos/", blank=True, null=True)
    city = models.CharField("Город", max_length=100, blank=True)

    # Verification
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    corporate_email = models.EmailField("Корпоративная почта", blank=True)
    inn = models.CharField("ИНН", max_length=20, blank=True)
    verification_note = models.TextField("Примечание куратора", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def __str__(self):
        return self.name

    @property
    def is_verified(self):
        return self.status == self.STATUS_VERIFIED
