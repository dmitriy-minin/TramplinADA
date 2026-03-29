"""
Management command: python manage.py create_demo_data

Создаёт разнообразные тестовые данные:
  - 6 работодателей (разные отрасли, статусы верификации)
  - 18 вакансий/стажировок/мероприятий/менторств
  - 8 соискателей (разные профили, навыки, курсы)
  - Отклики, контакты, избранное

Пароль для ВСЕХ тестовых аккаунтов: Demo12345!
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import date, timedelta
import random

User = get_user_model()
DEMO_PASSWORD = "Demo12345!"

EMPLOYERS = [
    {
        "email": "hr@kaspi-demo.kz",
        "display_name": "Айгуль Бекова — Kaspi Bank",
        "company": {
            "name": "Kaspi Bank", "industry": "fintech", "city": "Алматы",
            "description": "Ведущий финтех-банк Казахстана. Более 14 млн активных пользователей.",
            "website": "https://kaspi.kz", "corporate_email": "hr@kaspi.kz",
            "inn": "941240000978", "status": "verified",
        },
    },
    {
        "email": "hr@kolesa-demo.kz",
        "display_name": "Дмитрий Ли — Kolesa Group",
        "company": {
            "name": "Kolesa Group", "industry": "it", "city": "Алматы",
            "description": "Крупнейшая IT-компания Казахстана: Kolesa.kz, Krisha.kz, Market.kz.",
            "website": "https://kolesa-group.kz", "corporate_email": "hr@kolesa-group.kz",
            "inn": "050940003455", "status": "verified",
        },
    },
    {
        "email": "hr@epam-demo.kz",
        "display_name": "Наталья Смирнова — EPAM",
        "company": {
            "name": "EPAM Kazakhstan", "industry": "it", "city": "Алматы",
            "description": "Глобальная компания разработки ПО. Офисы в 50+ странах.",
            "website": "https://epam.com", "corporate_email": "hr@epam.com",
            "inn": "180340020891", "status": "verified",
        },
    },
    {
        "email": "hr@smartec-demo.kz",
        "display_name": "Асель Нурланова — Smartec IT",
        "company": {
            "name": "Smartec IT", "industry": "it", "city": "Астана",
            "description": "Разработка корпоративных ERP и CRM систем для крупного бизнеса.",
            "corporate_email": "hr@smartec.kz", "inn": "201140005512", "status": "verified",
        },
    },
    {
        "email": "hr@jusan-demo.kz",
        "display_name": "Ержан Сейтжанов — Jusan Tech",
        "company": {
            "name": "Jusan Tech", "industry": "fintech", "city": "Астана",
            "description": "Технологическое подразделение Jusan Bank. Строим цифровой банк будущего.",
            "website": "https://jusan.kz", "corporate_email": "hr@jusan.kz",
            "inn": "190340019234", "status": "pending",
        },
    },
    {
        "email": "hr@startupkz-demo.kz",
        "display_name": "Мадина Ахметова — StartupKZ",
        "company": {
            "name": "StartupKZ", "industry": "it", "city": "Алматы",
            "description": "Акселератор и продуктовая студия. Создаём IT-стартапы с нуля.",
            "corporate_email": "team@startupkz.io", "status": "rejected",
            "verification_note": "Не предоставлены документы о регистрации юридического лица.",
        },
    },
]

OPPORTUNITIES = [
    {"company_idx": 0, "title": "Python Backend Developer (Junior)",
     "opp_type": "vacancy", "work_format": "hybrid", "city": "Алматы", "lat": 43.2364, "lng": 76.9291,
     "salary_min": 350000, "salary_max": 550000, "contact_email": "hr@kaspi.kz",
     "description": "Разработка микросервисов для платёжной платформы Kaspi.\n\nТребования:\n- Python 3.10+\n- Django или FastAPI\n- PostgreSQL, Redis\n- Git, Docker базово\n\nУсловия:\n- Гибридный формат (3 дня офис)\n- ДМС с первого дня\n- Годовой бонус",
     "skills": ["Python", "Django", "SQL", "Git", "Docker"], "level": "Junior", "employment": "Полная занятость"},

    {"company_idx": 0, "title": "Data Analyst — Финансовая аналитика",
     "opp_type": "vacancy", "work_format": "office", "city": "Алматы", "lat": 43.2389, "lng": 76.8897,
     "salary_min": 400000, "salary_max": 650000, "contact_email": "hr@kaspi.kz",
     "description": "Анализ транзакционных данных и построение дашбордов.\n\nТребования:\n- SQL продвинутый\n- Python (Pandas, NumPy)\n- Tableau или Power BI\n- Статистика",
     "skills": ["SQL", "Python", "Data Science"], "level": "Junior", "employment": "Полная занятость"},

    {"company_idx": 0, "title": "Стажировка — Mobile iOS Developer",
     "opp_type": "internship", "work_format": "office", "city": "Алматы", "lat": 43.2220, "lng": 76.8512,
     "salary_min": 180000, "salary_max": 250000, "contact_email": "intern@kaspi.kz",
     "description": "6-месячная оплачиваемая стажировка в iOS-команде.\n\nЧто тебя ждёт:\n- Работа над приложением с 14 млн пользователей\n- Менторство от Senior iOS Developer\n- Возможность получить оффер\n\nТребования:\n- Swift основы\n- Студент или выпускник 2024-2025",
     "skills": ["iOS", "Swift"], "level": "Intern", "employment": "Стажировка оплачиваемая"},

    {"company_idx": 1, "title": "Frontend React Developer",
     "opp_type": "vacancy", "work_format": "remote", "city": "Алматы", "lat": 43.2550, "lng": 76.9126,
     "salary_min": 400000, "salary_max": 700000, "contact_email": "hr@kolesa-group.kz",
     "description": "Разработка интерфейсов для marketplace Kolesa.kz.\n\nТребования:\n- React 18+\n- TypeScript\n- REST API, GraphQL\n- Git\n\nУсловия:\n- Полностью удалённо\n- Гибкий график",
     "skills": ["React", "TypeScript", "JavaScript", "GraphQL", "Git"], "level": "Junior", "employment": "Полная занятость"},

    {"company_idx": 1, "title": "Go Backend Engineer",
     "opp_type": "vacancy", "work_format": "hybrid", "city": "Алматы", "lat": 43.2648, "lng": 76.9138,
     "salary_min": 600000, "salary_max": 900000, "contact_email": "hr@kolesa-group.kz",
     "description": "Разработка высоконагруженных сервисов на Go.\n\nТребования:\n- Go 1.20+\n- Микросервисная архитектура\n- PostgreSQL, Kafka\n- Docker, Kubernetes",
     "skills": ["Go", "Docker", "Kubernetes", "SQL"], "level": "Middle", "employment": "Полная занятость"},

    {"company_idx": 1, "title": "День открытых дверей — Kolesa Group",
     "opp_type": "event", "work_format": "office", "city": "Алматы", "lat": 43.2575, "lng": 76.9286,
     "salary_min": None, "salary_max": None, "contact_email": "hr@kolesa-group.kz",
     "event_delta_days": 14,
     "description": "Приглашаем студентов познакомиться с командой.\n\nПрограмма:\n10:00 — Презентация компании\n11:00 — Технические доклады\n12:30 — Обед с командой\n15:00 — Q&A сессия\n\nЛучшим — fast-track на собеседование!",
     "skills": ["JavaScript", "Python", "Go"], "level": None, "employment": None},

    {"company_idx": 2, "title": "Java Developer (Spring Boot)",
     "opp_type": "vacancy", "work_format": "remote", "city": "Алматы", "lat": 43.2489, "lng": 76.9200,
     "salary_min": 500000, "salary_max": 800000, "contact_email": "hr@epam.com",
     "description": "Разработка enterprise-приложений для международных клиентов.\n\nТребования:\n- Java 17+\n- Spring Boot, Spring MVC\n- Hibernate/JPA\n- PostgreSQL\n- Английский Upper-Intermediate+",
     "skills": ["Java", "SQL", "Git", "REST API"], "level": "Junior", "employment": "Полная занятость"},

    {"company_idx": 2, "title": "Стажировка — QA Automation Engineer",
     "opp_type": "internship", "work_format": "remote", "city": "Алматы", "lat": 43.2310, "lng": 76.9450,
     "salary_min": 150000, "salary_max": 200000, "contact_email": "internship@epam.com",
     "description": "Трёхмесячная стажировка в команде автоматизации тестирования.\n\nЧему научишься:\n- Selenium WebDriver\n- TestNG / JUnit\n- CI/CD интеграция\n\nТребования:\n- Базовые знания Java или Python\n- Студент 3+ курса",
     "skills": ["QA", "Selenium", "Java", "Python", "Postman"], "level": "Intern", "employment": "Стажировка оплачиваемая"},

    {"company_idx": 2, "title": "Менторская программа — Cloud & DevOps",
     "opp_type": "mentoring", "work_format": "online", "city": "Алматы", "lat": 43.2600, "lng": 76.9000,
     "salary_min": None, "salary_max": None, "contact_email": "mentoring@epam.com",
     "description": "10-недельная программа по DevOps и облачным технологиям.\n\nФормат: 2 встречи в неделю\n\nПрограмма:\n- Docker, Kubernetes\n- CI/CD pipelines\n- AWS основы\n- Мониторинг",
     "skills": ["Docker", "Kubernetes", "CI/CD", "Linux", "AWS"], "level": "Junior", "employment": None},

    {"company_idx": 3, "title": "Android Developer (Kotlin)",
     "opp_type": "vacancy", "work_format": "office", "city": "Астана", "lat": 51.1694, "lng": 71.4491,
     "salary_min": 450000, "salary_max": 750000, "contact_email": "hr@smartec.kz",
     "description": "Разработка корпоративного мобильного приложения.\n\nТребования:\n- Kotlin\n- Android SDK, Jetpack Compose\n- REST API\n- Git",
     "skills": ["Android", "Kotlin", "REST API", "Git"], "level": "Junior", "employment": "Полная занятость"},

    {"company_idx": 3, "title": "1C Разработчик",
     "opp_type": "vacancy", "work_format": "office", "city": "Астана", "lat": 51.1801, "lng": 71.4460,
     "salary_min": 350000, "salary_max": 500000, "contact_email": "hr@smartec.kz",
     "description": "Разработка и сопровождение решений на 1С:Предприятие 8.3.\n\nТребования:\n- 1С:Предприятие 8.3\n- Конфигурация БП, УТ\n- SQL базово",
     "skills": ["1C", "SQL"], "level": "Junior", "employment": "Полная занятость"},

    {"company_idx": 3, "title": "DevOps Engineer",
     "opp_type": "vacancy", "work_format": "hybrid", "city": "Астана", "lat": 51.1850, "lng": 71.4380,
     "salary_min": 600000, "salary_max": 950000, "contact_email": "hr@smartec.kz",
     "description": "Построение инфраструктуры и автоматизация деплоя.\n\nТребования:\n- Docker, Kubernetes\n- GitLab CI\n- Linux\n- Bash, Python",
     "skills": ["Docker", "Kubernetes", "CI/CD", "Linux", "Bash", "Python"], "level": "Middle", "employment": "Полная занятость"},

    {"company_idx": 4, "title": "Flutter Developer",
     "opp_type": "vacancy", "work_format": "hybrid", "city": "Астана", "lat": 51.1600, "lng": 71.4700,
     "salary_min": 500000, "salary_max": 800000, "contact_email": "hr@jusan.kz",
     "description": "Разработка мобильного банковского приложения на Flutter.\n\nТребования:\n- Flutter / Dart\n- REST API, WebSocket\n- BLoC или Riverpod\n- Git",
     "skills": ["Flutter", "REST API", "Git"], "level": "Junior", "employment": "Полная занятость"},

    {"company_idx": 4, "title": "Хакатон: FinTech Innovate 2025",
     "opp_type": "event", "work_format": "office", "city": "Астана", "lat": 51.1550, "lng": 71.4650,
     "salary_min": None, "salary_max": None, "contact_email": "hackathon@jusan.kz",
     "event_delta_days": 21,
     "description": "48-часовой хакатон по финансовым технологиям.\n\nПризовой фонд: 3 000 000 тенге\nКоманды: 3-5 человек\n\nТреки:\n- Open Banking API\n- AI в финансах\n- Кибербезопасность\n\nПобедители получат инвестиционное предложение.",
     "skills": ["Python", "JavaScript", "Machine Learning", "React"], "level": None, "employment": None},

    {"company_idx": 5, "title": "Full Stack Developer (React + Node.js)",
     "opp_type": "vacancy", "work_format": "remote", "city": "Алматы", "lat": 43.2700, "lng": 76.9400,
     "salary_min": 300000, "salary_max": 600000, "contact_email": "team@startupkz.io",
     "description": "Работа над стартап-продуктами.\n\nТребования:\n- React + TypeScript\n- Node.js + Express\n- MongoDB или PostgreSQL\n- Git",
     "skills": ["React", "JavaScript", "TypeScript", "SQL", "Git"], "level": "Junior", "employment": "Проектная работа"},

    {"company_idx": 5, "title": "Менторская программа — Продуктовый дизайн",
     "opp_type": "mentoring", "work_format": "online", "city": "Алматы", "lat": 43.2450, "lng": 76.8900,
     "salary_min": None, "salary_max": None, "contact_email": "design@startupkz.io",
     "description": "8-недельная программа для начинающих UX/UI дизайнеров.\n\nПрограмма:\n- User research, CJM\n- Figma (компоненты, auto layout)\n- Прототипирование\n- Design system\n\nФормат: 2 встречи в неделю",
     "skills": ["Figma", "UI/UX"], "level": "Trainee", "employment": None},
]

APPLICANTS = [
    {"email": "aiya.bekova@demo.kz", "display_name": "Айя Бекова",
     "full_name": "Бекова Айя Нурлановна", "university": "КБТУ", "graduation_year": 2025,
     "skills": "Python, Django, FastAPI, PostgreSQL, Git, Docker, Linux",
     "bio": "Студентка 4 курса, направление «Компьютерные науки». Ищу стажировку или первую работу в продуктовой компании.",
     "experience": "Дипломный проект: REST API сервис на FastAPI + PostgreSQL.\nХакатон Digital Almaty 2024 — 2 место в треке AI.\nТелеграм-бот для учёта финансов.",
     "github_url": "https://github.com/aiya-bekova", "profile_public": True, "hide_applications": False},

    {"email": "arman.seitkali@demo.kz", "display_name": "Арман Сейткали",
     "full_name": "Сейткали Арман Болатович", "university": "МУИТ", "graduation_year": 2024,
     "skills": "JavaScript, TypeScript, React, Vue.js, Node.js, Git, HTML, CSS",
     "bio": "Выпускник 2024. Специализируюсь на frontend. Открыт к relocate.",
     "experience": "3 лендинга на React для казахстанских стартапов.\nСистема управления задачами (React + Node.js + MongoDB).\nСтажировка в WebKaz — вёрстка шаблонов.",
     "github_url": "https://github.com/arman-seitkali",
     "portfolio_url": "https://arman.dev", "profile_public": True, "hide_applications": False},

    {"email": "dana.nurlan@demo.kz", "display_name": "Дана Нурланова",
     "full_name": "Нурланова Дана Ержановна", "university": "КазНУ им. аль-Фараби", "graduation_year": 2026,
     "skills": "Python, Machine Learning, Pandas, NumPy, Scikit-learn, SQL, Jupyter",
     "bio": "Студентка 3 курса, мехмат. Специализируюсь на Data Science и ML.",
     "experience": "Прогнозирование временных рядов (Keras, LSTM).\nKaggle — топ-15% в соревновании по классификации.\nАнализ рынка недвижимости Алматы.",
     "github_url": "https://github.com/dana-nurlan", "profile_public": True, "hide_applications": True},

    {"email": "timur.rakhimov@demo.kz", "display_name": "Тимур Рахимов",
     "full_name": "Рахимов Тимур Алмасович", "university": "Nazarbayev University", "graduation_year": 2025,
     "skills": "Java, Spring Boot, Kotlin, Android, PostgreSQL, Docker, Git, REST API",
     "bio": "Студент Computer Science. Разрабатываю Android и backend на Java/Kotlin.",
     "experience": "Android-приложение для студенческого расписания (Kotlin + Spring Boot).\nСтажировка в Kolesa (1 месяц).\nКонтрибьюции в opensource.",
     "github_url": "https://github.com/timur-rakhimov", "profile_public": True, "hide_applications": False},

    {"email": "zhansaya.omar@demo.kz", "display_name": "Жансая Омар",
     "full_name": "Омар Жансая Сейткалиевна", "university": "Алматы Менеджмент Университет", "graduation_year": 2024,
     "skills": "QA, Selenium, Postman, Jira, SQL, Python, Тест-кейсы, Баг-репорты",
     "bio": "Выпускница по специальности «Информационные системы». Сертификат ISTQB Foundation.",
     "experience": "Курсы QA Automation (Practicum) — Selenium + Python.\nТестирование мобильного приложения.\nСоставление тест-кейсов для e-commerce.",
     "profile_public": False, "hide_applications": True},

    {"email": "bekzat.akhmet@demo.kz", "display_name": "Бекзат Ахметов",
     "full_name": "Ахметов Бекзат Ерланович", "university": "ЕНУ им. Л.Н. Гумилёва", "graduation_year": 2026,
     "skills": "C++, Python, Linux, Bash, Git",
     "bio": "Студент 2 курса, программная инженерия. Увлекаюсь системным программированием и Linux.",
     "experience": "Реализация стека TCP/IP на C++.\nНастройка домашнего сервера (Ubuntu, Nginx, PostgreSQL).",
     "github_url": "https://github.com/bekzat-akhmet", "profile_public": True, "hide_applications": False},

    {"email": "alina.kim@demo.kz", "display_name": "Алина Ким",
     "full_name": "Ким Алина Вадимовна", "university": "Университет «Туран»", "graduation_year": 2025,
     "skills": "Figma, UI/UX, HTML, CSS, Adobe XD, Прототипирование, User Research",
     "bio": "Дизайнер с фокусом на UI/UX. Создаю интерфейсы для мобильных приложений и веб.",
     "experience": "Редизайн приложения для заказа еды — полный UX-цикл.\n3 коммерческих проекта на фрилансе.\nGoogle UX Design Certificate.",
     "portfolio_url": "https://alina-kim.design", "profile_public": True, "hide_applications": False},

    {"email": "ruslan.dyusembaev@demo.kz", "display_name": "Руслан Дюсембаев",
     "full_name": "Дюсембаев Руслан Маратович", "university": "Satbayev University", "graduation_year": 2023,
     "skills": "Python, Django, REST API, PostgreSQL, Redis, Celery, Docker, Git, Linux",
     "bio": "Выпускник 2023, 8 месяцев коммерческой разработки. Ищу Junior+ или Middle Python Developer.",
     "experience": "8 месяцев backend в стартапе EduKZ: DRF, Celery, PostgreSQL.\nИнтеграция с Kaspi Pay API.\nSaaS-платформа для управления проектами.",
     "github_url": "https://github.com/ruslan-dyusembaev",
     "resume_url": "https://hh.kz/resume/ruslan-dyusembaev", "profile_public": True, "hide_applications": False},
]


class Command(BaseCommand):
    help = "Create diverse demo data for thorough testing"

    def handle(self, *args, **options):
        from apps.companies.models import Company
        from apps.opportunities.models import Opportunity, Tag, Application

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("  Создание тестовых данных Трамплин")
        self.stdout.write("=" * 60)

        company_objects = self._create_employers()
        self._create_opportunities(company_objects)
        applicant_objects = self._create_applicants()
        self._create_applications(applicant_objects)
        self._create_contacts(applicant_objects)
        self._print_summary()

    def _upsert_user(self, email, display_name, role, extra=None):
        from apps.accounts.models import User as UserModel
        role_map = {
            "applicant": UserModel.ROLE_APPLICANT,
            "employer": UserModel.ROLE_EMPLOYER,
            "curator": UserModel.ROLE_CURATOR,
        }
        defaults = {"username": email, "display_name": display_name,
                    "role": role_map[role], **(extra or {})}
        user, _ = User.objects.update_or_create(email=email, defaults=defaults)
        # Всегда сбрасываем пароль — ключевое исправление
        user.set_password(DEMO_PASSWORD)
        user.save(update_fields=["password"])
        return user

    def _create_employers(self):
        from apps.companies.models import Company
        company_objects = []
        self.stdout.write("\n📦 Работодатели:")
        for e in EMPLOYERS:
            user = self._upsert_user(e["email"], e["display_name"], "employer")
            c = e["company"]
            company, _ = Company.objects.update_or_create(
                owner=user,
                defaults={
                    "name": c["name"], "industry": c["industry"], "city": c.get("city", ""),
                    "description": c.get("description", ""), "website": c.get("website", ""),
                    "corporate_email": c.get("corporate_email", ""), "inn": c.get("inn", ""),
                    "status": c.get("status", "verified"),
                    "verification_note": c.get("verification_note", ""),
                },
            )
            company_objects.append(company)
            icon = {"verified": "✅", "pending": "⏳", "rejected": "❌"}.get(company.status, "•")
            self.stdout.write(f"  {icon} {company.name}")
        return company_objects

    def _create_opportunities(self, company_objects):
        from apps.opportunities.models import Opportunity, Tag
        from django.utils import timezone
        self.stdout.write("\n💼 Вакансии:")
        for o in OPPORTUNITIES:
            company = company_objects[o["company_idx"]]
            event_date = None
            if o.get("event_delta_days"):
                event_date = timezone.now() + timedelta(days=o["event_delta_days"])
            opp, _ = Opportunity.objects.update_or_create(
                company=company, title=o["title"],
                defaults={
                    "opp_type": o["opp_type"], "work_format": o["work_format"],
                    "city": o["city"], "latitude": o.get("lat"), "longitude": o.get("lng"),
                    "salary_min": o.get("salary_min"), "salary_max": o.get("salary_max"),
                    "salary_currency": "KZT", "description": o["description"],
                    "status": Opportunity.STATUS_ACTIVE, "is_moderated": True,
                    "expires_at": date.today() + timedelta(days=45),
                    "event_date": event_date, "contact_email": o.get("contact_email", ""),
                },
            )
            opp.tags.clear()
            for name in (o.get("skills") or []):
                tag = Tag.objects.filter(name=name).first()
                if tag:
                    opp.tags.add(tag)
            for field, ttype in [("level", Tag.TAG_TYPE_LEVEL), ("employment", Tag.TAG_TYPE_EMPLOYMENT)]:
                if o.get(field):
                    tag = Tag.objects.filter(name=o[field], tag_type=ttype).first()
                    if tag:
                        opp.tags.add(tag)
            icon = {"vacancy": "💼", "internship": "🎓", "event": "📅", "mentoring": "🤝"}.get(o["opp_type"], "•")
            self.stdout.write(f"  {icon} {o['title']}")

    def _create_applicants(self):
        applicant_objects = []
        self.stdout.write("\n👤 Соискатели:")
        for a in APPLICANTS:
            extra = {k: a.get(k, "") for k in
                     ["full_name", "university", "graduation_year", "skills", "bio",
                      "experience", "github_url", "portfolio_url", "resume_url",
                      "profile_public", "hide_applications"]}
            user = self._upsert_user(a["email"], a["display_name"], "applicant", extra)
            applicant_objects.append(user)
            privacy = "🔓" if a["profile_public"] else "🔒"
            self.stdout.write(f"  {privacy} {a['display_name']}")
        return applicant_objects

    def _create_applications(self, applicants):
        from apps.opportunities.models import Opportunity, Application
        self.stdout.write("\n📨 Отклики:")
        opps = list(Opportunity.objects.filter(is_moderated=True))
        if not opps:
            return
        random.seed(42)
        statuses = [Application.STATUS_PENDING, Application.STATUS_ACCEPTED,
                    Application.STATUS_REJECTED, Application.STATUS_RESERVE]
        count = 0
        for i, applicant in enumerate(applicants):
            sample = random.sample(opps, min(3, len(opps)))
            for j, opp in enumerate(sample):
                _, created = Application.objects.get_or_create(
                    applicant=applicant, opportunity=opp,
                    defaults={
                        "status": statuses[(i + j) % len(statuses)],
                        "cover_letter": f"Здравствуйте! Меня очень заинтересовала позиция «{opp.title}».",
                        "is_favorite": j == 0,
                    },
                )
                if created:
                    count += 1
        self.stdout.write(f"  Создано {count} откликов")

    def _create_contacts(self, applicants):
        self.stdout.write("\n👥 Контакты:")
        if len(applicants) >= 4:
            applicants[0].contacts.add(applicants[1])
            applicants[0].contacts.add(applicants[2])
            applicants[1].contacts.add(applicants[3])
            applicants[2].contacts.add(applicants[3])
        self.stdout.write("  Добавлено 4 пары контактов")

    def _print_summary(self):
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("  ✅ Готово! Все тестовые аккаунты:"))
        self.stdout.write("=" * 60)
        self.stdout.write(f"\n  Единый пароль тестовых аккаунтов: {DEMO_PASSWORD}\n")

        self.stdout.write("  ── АДМИНИСТРАТОР ──────────────────────────────────────")
        self.stdout.write("  admin@tramplin.kz                    / Admin123!@#\n")

        self.stdout.write("  ── РАБОТОДАТЕЛИ ───────────────────────────────────────")
        for e in EMPLOYERS:
            s = e["company"].get("status", "verified")
            lbl = {"verified": "✅ верифицирован", "pending": "⏳ на проверке", "rejected": "❌ отклонён"}.get(s, "")
            self.stdout.write(f"  {e['email']:<40} / {DEMO_PASSWORD}  {lbl}")

        self.stdout.write("\n  ── СОИСКАТЕЛИ ─────────────────────────────────────────")
        for a in APPLICANTS:
            p = "🔓 публичный" if a["profile_public"] else "🔒 скрытый"
            self.stdout.write(f"  {a['email']:<40} / {DEMO_PASSWORD}  {p}")

        self.stdout.write("\n" + "=" * 60 + "\n")
