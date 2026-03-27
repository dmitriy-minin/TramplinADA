"""
Management command: python manage.py create_demo_data

Creates sample companies, opportunities and users for demonstration.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import random
from datetime import date, timedelta

User = get_user_model()

COMPANIES = [
    {"name": "Kaspi Bank", "industry": "fintech", "city": "Алматы",
     "description": "Ведущий финтех-банк Казахстана.", "website": "https://kaspi.kz",
     "corporate_email": "hr@kaspi.kz"},
    {"name": "Kolesa Group", "industry": "it", "city": "Алматы",
     "description": "Крупнейшая IT-компания Казахстана — Kolesa.kz, Krisha.kz, Market.kz.",
     "website": "https://kolesa-group.kz", "corporate_email": "hr@kolesa-group.kz"},
    {"name": "EPAM Kazakhstan", "industry": "it", "city": "Алматы",
     "description": "Глобальная компания разработки ПО.",
     "website": "https://epam.com", "corporate_email": "hr@epam.com"},
    {"name": "Smartec IT", "industry": "it", "city": "Астана",
     "description": "Разработка корпоративных IT-решений.",
     "corporate_email": "hr@smartec.kz"},
]

OPPORTUNITIES = [
    {"title": "Python Backend Developer (Junior)", "opp_type": "vacancy", "work_format": "hybrid",
     "salary_min": 350000, "salary_max": 550000, "city": "Алматы",
     "lat": 43.238949, "lng": 76.889709,
     "description": "Ищем Junior Python-разработчика в команду бэкенд.\n\n"
                    "Требования:\n- Python 3.10+\n- Django или FastAPI\n- SQL основы\n- Git\n\n"
                    "Условия:\n- Гибкий график\n- ДМС\n- Обучение за счёт компании",
     "skills": ["Python", "Django", "SQL", "Git"], "level": "Junior"},

    {"title": "Frontend React Developer", "opp_type": "vacancy", "work_format": "remote",
     "salary_min": 400000, "salary_max": 700000, "city": "Алматы",
     "lat": 43.2220, "lng": 76.8512,
     "description": "Разработка веб-приложений на React.\n\n"
                    "Требования:\n- React 18+\n- TypeScript\n- REST API\n- Git\n\n"
                    "Условия:\n- Полностью удалённо\n- Гибкий график\n- Международный опыт",
     "skills": ["React", "TypeScript", "JavaScript", "Git"], "level": "Junior"},

    {"title": "Летняя стажировка — Data Science", "opp_type": "internship", "work_format": "office",
     "salary_min": 150000, "salary_max": 250000, "city": "Алматы",
     "lat": 43.2364, "lng": 76.9457,
     "description": "3-месячная оплачиваемая стажировка в команде аналитики.\n\n"
                    "Требования:\n- Python основы\n- Pandas, NumPy\n- Статистика\n- Студент 3-4 курса\n\n"
                    "Вы получите:\n- Реальные проекты\n- Менторство\n- Возможность оффера",
     "skills": ["Python", "Machine Learning", "Data Science", "SQL"], "level": "Intern"},

    {"title": "DevOps Engineer", "opp_type": "vacancy", "work_format": "hybrid",
     "salary_min": 600000, "salary_max": 900000, "city": "Астана",
     "lat": 51.1801, "lng": 71.4460,
     "description": "Построение и поддержка CI/CD pipelines.\n\n"
                    "Требования:\n- Docker, Kubernetes\n- CI/CD (GitLab/GitHub)\n- Linux\n- Bash\n\n"
                    "Условия:\n- ДМС\n- Релокация в Астану",
     "skills": ["Docker", "Kubernetes", "CI/CD", "Linux", "Bash"], "level": "Middle"},

    {"title": "Хакатон: AI for Good", "opp_type": "event", "work_format": "office",
     "salary_min": None, "salary_max": None, "city": "Алматы",
     "lat": 43.2575, "lng": 76.9286,
     "description": "48-часовой хакатон по разработке AI-решений для социальных задач.\n\n"
                    "Призовой фонд: 1 000 000 тенге\n"
                    "Участники: команды 2-4 человека\n\n"
                    "Треки:\n- Здравоохранение\n- Образование\n- Экология",
     "skills": ["Python", "Machine Learning", "JavaScript"], "level": None},

    {"title": "Менторская программа — Backend", "opp_type": "mentoring", "work_format": "online",
     "salary_min": None, "salary_max": None, "city": "Алматы",
     "lat": 43.2550, "lng": 76.9126,
     "description": "12-недельная менторская программа от Senior-разработчиков.\n\n"
                    "Формат: 1 встреча в неделю + ревью кода\n"
                    "Цель: вырасти с Trainee до Junior за 3 месяца\n\n"
                    "Требования:\n- Python или JavaScript базовые знания\n- Мотивация расти",
     "skills": ["Python", "Django", "Git"], "level": "Trainee"},

    {"title": "Android Developer (Kotlin)", "opp_type": "vacancy", "work_format": "office",
     "salary_min": 450000, "salary_max": 750000, "city": "Астана",
     "lat": 51.1694, "lng": 71.4491,
     "description": "Разработка мобильного приложения на Kotlin.\n\n"
                    "Требования:\n- Kotlin\n- Android SDK\n- REST API интеграция\n- Git\n\n"
                    "Условия:\n- Современный офис\n- ДМС\n- Корпоративное питание",
     "skills": ["Android", "Kotlin", "REST API", "Git"], "level": "Junior"},

    {"title": "QA Engineer", "opp_type": "vacancy", "work_format": "remote",
     "salary_min": 280000, "salary_max": 450000, "city": "Алматы",
     "lat": 43.2648, "lng": 76.9138,
     "description": "Ручное и автоматизированное тестирование веб-приложений.\n\n"
                    "Требования:\n- Основы тестирования\n- Postman\n- Базовый Python или JS\n- Selenium желательно",
     "skills": ["QA", "Selenium", "Postman", "Python"], "level": "Junior"},
]


class Command(BaseCommand):
    help = "Create demo data for testing/presentation"

    def handle(self, *args, **options):
        from apps.companies.models import Company
        from apps.opportunities.models import Opportunity, Tag

        self.stdout.write("Creating demo data...")

        # Create employer users and companies
        company_objects = []
        for i, c_data in enumerate(COMPANIES):
            email = f"employer{i+1}@demo.tramplin.kz"
            user, _ = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": email,
                    "display_name": f"HR — {c_data['name']}",
                    "role": User.ROLE_EMPLOYER,
                }
            )
            if not user.has_usable_password():
                user.set_password("Demo12345!")
                user.save()

            company, created = Company.objects.get_or_create(
                owner=user,
                defaults={
                    "name": c_data["name"],
                    "industry": c_data["industry"],
                    "city": c_data["city"],
                    "description": c_data.get("description", ""),
                    "website": c_data.get("website", ""),
                    "corporate_email": c_data.get("corporate_email", ""),
                    "status": Company.STATUS_VERIFIED,
                }
            )
            if not created:
                company.status = Company.STATUS_VERIFIED
                company.save(update_fields=["status"])
            company_objects.append(company)
            self.stdout.write(f"  Company: {company.name}")

        # Create opportunities
        for i, o_data in enumerate(OPPORTUNITIES):
            company = company_objects[i % len(company_objects)]
            opp, created = Opportunity.objects.get_or_create(
                company=company,
                title=o_data["title"],
                defaults={
                    "opp_type": o_data["opp_type"],
                    "work_format": o_data["work_format"],
                    "city": o_data["city"],
                    "latitude": o_data.get("lat"),
                    "longitude": o_data.get("lng"),
                    "salary_min": o_data.get("salary_min"),
                    "salary_max": o_data.get("salary_max"),
                    "salary_currency": "KZT",
                    "description": o_data["description"],
                    "status": Opportunity.STATUS_ACTIVE,
                    "is_moderated": True,
                    "expires_at": date.today() + timedelta(days=30),
                    "contact_email": company.corporate_email or f"hr@demo.kz",
                }
            )
            if created:
                # Add skill tags
                for skill_name in o_data.get("skills", []):
                    tag = Tag.objects.filter(name=skill_name).first()
                    if tag:
                        opp.tags.add(tag)
                # Add level tag
                if o_data.get("level"):
                    level_tag = Tag.objects.filter(name=o_data["level"], tag_type=Tag.TAG_TYPE_LEVEL).first()
                    if level_tag:
                        opp.tags.add(level_tag)
                # Full employment tag for vacancies
                if o_data["opp_type"] == "vacancy":
                    emp_tag = Tag.objects.filter(name="Полная занятость").first()
                    if emp_tag:
                        opp.tags.add(emp_tag)
                self.stdout.write(f"  Opportunity: {opp.title}")

        # Create demo applicant
        applicant_email = "student@demo.tramplin.kz"
        applicant, _ = User.objects.get_or_create(
            email=applicant_email,
            defaults={
                "username": applicant_email,
                "display_name": "Алия Демо",
                "full_name": "Алия Демо Студент",
                "role": User.ROLE_APPLICANT,
                "university": "КБТУ",
                "graduation_year": 2025,
                "skills": "Python, Django, SQL, Git, JavaScript",
                "bio": "Студентка 4 курса КБТУ. Ищу стажировку в сфере backend-разработки.",
                "experience": "Учебные проекты: Django REST API, простой чат-бот на Python.",
                "profile_public": True,
            }
        )
        if not applicant.has_usable_password():
            applicant.set_password("Demo12345!")
            applicant.save()
        self.stdout.write(f"  Applicant: {applicant_email} / Demo12345!")

        self.stdout.write(self.style.SUCCESS(
            "\n✅ Demo data created!\n"
            "  Admin:     admin@tramplin.kz / Admin123!@#\n"
            "  Employer:  employer1@demo.tramplin.kz / Demo12345!\n"
            "  Applicant: student@demo.tramplin.kz / Demo12345!"
        ))
