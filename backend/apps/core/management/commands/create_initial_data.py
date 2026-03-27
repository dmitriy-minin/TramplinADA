"""
Management command: python manage.py create_initial_data

Creates:
  - Admin curator account (admin@tramplin.kz / Admin123!@#)
  - System tags (skills, levels, employment types)
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

SKILL_TAGS = [
    "Python", "Django", "FastAPI", "Flask",
    "JavaScript", "TypeScript", "React", "Vue.js", "Next.js",
    "Java", "Spring Boot", "Kotlin",
    "C++", "C#", ".NET",
    "Go", "Rust", "Swift",
    "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis",
    "Docker", "Kubernetes", "CI/CD", "Git",
    "Machine Learning", "Deep Learning", "Data Science",
    "Linux", "Bash", "REST API", "GraphQL",
    "HTML", "CSS", "Figma", "UI/UX",
    "Android", "iOS", "Flutter", "React Native",
    "QA", "Selenium", "Pytest", "Postman",
    "DevOps", "AWS", "GCP", "Azure",
    "1C", "SAP", "Bitrix",
]

LEVEL_TAGS = [
    "Intern", "Junior", "Middle", "Senior", "Lead", "Trainee",
]

EMPLOYMENT_TAGS = [
    "Полная занятость", "Частичная занятость",
    "Проектная работа", "Волонтёрство", "Стажировка оплачиваемая",
]


class Command(BaseCommand):
    help = "Create initial data: admin curator and system tags"

    def handle(self, *args, **options):
        self._create_admin()
        self._create_tags()
        self.stdout.write(self.style.SUCCESS("✅ Initial data created successfully."))

    def _create_admin(self):
        from apps.curator.models import CuratorProfile

        email = "admin@tramplin.kz"
        password = "Admin123!@#"

        if User.objects.filter(email=email).exists():
            self.stdout.write(f"  Admin already exists: {email}")
            return

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            display_name="Главный администратор",
            role=User.ROLE_CURATOR,
            is_staff=True,
        )
        CuratorProfile.objects.create(
            user=user,
            university="Трамплин",
            position="Администратор платформы",
            is_admin=True,
        )
        self.stdout.write(
            self.style.SUCCESS(f"  Created admin: {email} / {password}")
        )

    def _create_tags(self):
        from apps.opportunities.models import Tag

        created = 0
        for name in SKILL_TAGS:
            _, ok = Tag.objects.get_or_create(
                name=name,
                defaults={"tag_type": Tag.TAG_TYPE_SKILL, "is_system": True},
            )
            if ok:
                created += 1

        for name in LEVEL_TAGS:
            _, ok = Tag.objects.get_or_create(
                name=name,
                defaults={"tag_type": Tag.TAG_TYPE_LEVEL, "is_system": True},
            )
            if ok:
                created += 1

        for name in EMPLOYMENT_TAGS:
            _, ok = Tag.objects.get_or_create(
                name=name,
                defaults={"tag_type": Tag.TAG_TYPE_EMPLOYMENT, "is_system": True},
            )
            if ok:
                created += 1

        self.stdout.write(f"  Created {created} new system tags.")
