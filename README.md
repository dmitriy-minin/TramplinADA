# 🚀 Трамплин - Карьерная платформа для IT

Полнофункциональная карьерная экосистема для студентов, выпускников, работодателей и кураторов вузов в сфере IT и смежных областях.

**Стек:** Python 3.11+, Django 5.2, Django REST Framework, PostgreSQL / SQLite, MapLibre GL JS, CARTO Basemaps<br>
**Разработчики:** Минин Дмитрий, Максутов Азамат, Айджан Амалия. Команда из 3-х junior-разработчиков, студенты ЗКАТУ им. Жангир хана города Уральска. 

---

## Быстрый старт

### Вариант 1: Docker (рекомендуется)

```bash
cp .env.example .env
docker compose up --build
```

После запуска:
- http://127.0.0.1:8000/ - главная страница
- http://127.0.0.1:8000/api/health/ - health check

### Вариант 2: Локально (SQLite, без Docker)

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cd backend
python manage.py migrate
python manage.py create_initial_data   # admin + 60+ системных тегов
python manage.py create_demo_data      # тестовые данные (опционально)
python manage.py runserver
```

### Вариант 3: Локально с PostgreSQL

```bash
export DB_ENGINE=postgres
export POSTGRES_DB=tramplin_db
export POSTGRES_USER=tramplin_user
export POSTGRES_PASSWORD=tramplin_password
export POSTGRES_HOST=127.0.0.1
export POSTGRES_PORT=5432

cd backend
python manage.py migrate
python manage.py create_initial_data
python manage.py runserver
```

---

## Аккаунты

### После `create_initial_data`

| Роль | Email | Пароль |
|---|---|---|
| Администратор (куратор) | `admin@tramplin.kz` | `Admin123!@#` |

### После `create_demo_data` - полный список тестовых аккаунтов

Единый пароль для всех тестовых аккаунтов: **`Demo12345!`**

#### Работодатели

| Email | Компания | Статус верификации |
|---|---|---|
| `hr@kaspi-demo.kz` | Kaspi Bank | ✅ Верифицирован |
| `hr@kolesa-demo.kz` | Kolesa Group | ✅ Верифицирован |
| `hr@epam-demo.kz` | EPAM Kazakhstan | ✅ Верифицирован |
| `hr@smartec-demo.kz` | Smartec IT | ✅ Верифицирован |
| `hr@jusan-demo.kz` | Jusan Tech | ⏳ На проверке |
| `hr@startupkz-demo.kz` | StartupKZ | ❌ Отклонён |

#### Соискатели

| Email | Имя | Город | Профиль |
|---|---|---|---|
| `aiya.bekova@demo.kz` | Айя Бекова | Алматы | 🔓 Публичный |
| `arman.seitkali@demo.kz` | Арман Сейткали | Алматы | 🔓 Публичный |
| `dana.nurlan@demo.kz` | Дана Нурланова | Алматы | 🔓 Публичный |
| `timur.rakhimov@demo.kz` | Тимур Рахимов | Астана | 🔓 Публичный |
| `zhansaya.omar@demo.kz` | Жансая Омар | Алматы | 🔒 Скрытый |
| `bekzat.akhmet@demo.kz` | Бекзат Ахметов | Астана | 🔓 Публичный |
| `alina.kim@demo.kz` | Алина Ким | Алматы | 🔓 Публичный |
| `ruslan.dyusembaev@demo.kz` | Руслан Дюсембаев | Алматы | 🔓 Публичный |

---

## Структура проекта

```
TramplinADA/
├── requirements.txt
├── docker-compose.yml
├── .env.example
└── backend/
    ├── manage.py
    ├── config/
    │   ├── settings.py          # Настройки Django
    │   ├── urls.py              # Главный URL-роутер
    │   ├── wsgi.py
    │   └── asgi.py
    ├── apps/
    │   ├── core/                # Главная страница, management commands, template tags
    │   │   ├── views.py
    │   │   ├── templatetags/
    │   │   │   └── tramplin_tags.py   # Кастомные фильтры: split_skills, trim
    │   │   └── management/commands/
    │   │       ├── create_initial_data.py
    │   │       └── create_demo_data.py
    │   ├── accounts/            # Пользователи, аутентификация, каталог
    │   │   ├── models.py        # User (кастомный AUTH_USER_MODEL)
    │   │   ├── views.py
    │   │   ├── forms.py
    │   │   ├── urls.py          # /auth/*
    │   │   └── applicant_urls.py  # /dashboard/applicant/*
    │   ├── companies/           # Компании и верификация
    │   │   ├── models.py        # Company
    │   │   └── forms.py
    │   ├── opportunities/       # Вакансии, теги, отклики
    │   │   ├── models.py        # Tag, Opportunity, Application
    │   │   ├── views.py
    │   │   ├── forms.py
    │   │   ├── urls.py          # /opportunities/*
    │   │   ├── employer_urls.py # /dashboard/employer/*
    │   │   └── api_urls.py      # /api/*
    │   └── curator/             # Панель куратора
    │       ├── models.py        # CuratorProfile
    │       ├── views.py
    │       └── urls.py          # /curator/*
    ├── templates/
    │   ├── base.html
    │   ├── core/index.html      # Главная страница с картой
    │   ├── accounts/            # login, register, dashboard, catalog, profile
    │   ├── opportunities/       # list, detail, form, employer, applicants
    │   └── curator/             # dashboard, companies, opportunities, users, tags
    ├── static/
    │   ├── css/main.css         # Дизайн-система (~700 строк)
    │   └── js/main.js           # Клиентская логика
    └── scripts/entrypoint.sh
```

---

## Маршруты (URL)

| URL | Описание |
|---|---|
| `/` | Главная: карта + список вакансий |
| `/opportunities/` | Все вакансии с фильтрами |
| `/opportunities/<id>/` | Детали вакансии + форма отклика |
| `/auth/login/` | Вход |
| `/auth/logout/` | Выход (POST) |
| `/auth/register/` | Выбор роли при регистрации |
| `/auth/register/applicant/` | Регистрация соискателя |
| `/auth/register/employer/` | Регистрация работодателя |
| `/auth/contact/<id>/request/` | Отправить заявку в контакты (POST) |
| `/auth/contact/<id>/accept/` | Принять заявку в контакты (POST) |
| `/dashboard/` | Редирект в нужный кабинет |
| `/dashboard/applicant/` | Кабинет соискателя |
| `/dashboard/applicant/profile/` | Редактирование профиля |
| `/dashboard/applicant/catalog/` | Каталог специалистов (нетворкинг) |
| `/dashboard/employer/` | Кабинет работодателя |
| `/dashboard/employer/company/` | Редактирование профиля компании |
| `/dashboard/employer/create/` | Создать вакансию |
| `/dashboard/employer/<id>/edit/` | Редактировать вакансию |
| `/dashboard/employer/<id>/applicants/` | Отклики на вакансию |
| `/dashboard/employer/application/<id>/status/` | Изменить статус отклика (POST) |
| `/curator/` | Панель куратора |
| `/curator/companies/` | Верификация компаний |
| `/curator/companies/<id>/verify/` | Верифицировать / отклонить компанию (POST) |
| `/curator/opportunities/` | Модерация вакансий |
| `/curator/opportunities/<id>/moderate/` | Одобрить / отклонить вакансию (POST) |
| `/curator/users/` | Управление пользователями |
| `/curator/users/<id>/` | Профиль пользователя |
| `/curator/users/<id>/toggle/` | Блокировать / разблокировать (POST) |
| `/curator/tags/` | Управление тегами |
| `/curator/tags/create/` | Создать тег (POST) |
| `/curator/tags/<id>/delete/` | Удалить тег (POST) |
| `/curator/curators/` | Список кураторов (только admin) |
| `/curator/curators/create/` | Создать куратора (только admin, POST) |
| `/profile/<id>/` | Публичный профиль соискателя |
| `/api/health/` | Health check |
| `/api/map-markers/` | JSON-маркеры для карты |

---

## Модели данных

### User (accounts)
- **Роли:** `applicant` | `employer` | `curator`
- **Поля соискателя:** ФИО, вуз, год выпуска, **город**, навыки (через запятую), опыт, GitHub, портфолио, резюме
- **Приватность:** `profile_public` - профиль виден всем; `hide_applications` - скрыть отклики от контактов
- **Контакты:** M2M `contacts` (взаимные) + `contact_requests` (асимметричные заявки)

### Company (companies)
- **Верификация:** `pending` → `verified` | `rejected`
- **Поля:** название, отрасль, описание, город, сайт, LinkedIn, Telegram, HH, корп. почта, ИНН, примечание куратора

### Tag (opportunities)
- **Типы:** `skill` (Python, React...) | `level` (Junior, Middle...) | `employment` (полная, частичная...)
- 60+ системных тегов создаются командой `create_initial_data`
- Работодатели и кураторы могут добавлять собственные теги

### Opportunity (opportunities)
- **Типы:** `internship` | `vacancy` | `mentoring` | `event`
- **Форматы:** `office` | `hybrid` | `remote` | `online`
- **Статусы:** `active` | `closed` | `planned` | `draft`
- **Геолокация:** `latitude`, `longitude` - отображение на карте MapLibre GL
- **Модерация:** `is_moderated=False` → куратор одобряет перед публикацией

### Application (opportunities)
- **Статусы:** `pending` → `accepted` | `rejected` | `reserve`
- `is_favorite` - добавлено в избранное соискателем

### CuratorProfile (curator)
- Связан `OneToOne` с `User`
- `is_admin=True` - только этот куратор может создавать других кураторов

---

## Функциональность

### Публичная часть (без регистрации)
- Просмотр вакансий на карте (MapLibre GL + CARTO Basemaps, без ключей)
- Переключение: карта / сетка / список
- Фильтрация по типу, формату, навыкам, зарплате, городу
- Детальная страница вакансии

### Соискатель
- Регистрация → профиль с городом, резюме, навыками, ссылками
- Отклик с сопроводительным письмом
- Избранное, история откликов со статусами
- Публичный профиль с настройками приватности
- **Каталог специалистов** (`/dashboard/applicant/catalog/`) - поиск по имени, навыку, городу, вузу; сортировка; кнопка «+ Добавить» напрямую из каталога
- Добавление контактов: заявка → принятие → взаимные контакты

### Работодатель
- Регистрация + создание компании → верификация куратором
- Создание и редактирование вакансий/мероприятий
- Выбор координат кликом по карте при создании
- Управление откликами: принять / отклонить / в резерв
- Просмотр профилей, GitHub и резюме соискателей

### Куратор
- Верификация компаний (корп. почта, ИНН) с примечанием
- Модерация вакансий с примечанием
- Просмотр и блокировка пользователей
- Управление тегами
- **Только администратор** (`is_admin=True`) создаёт аккаунты других кураторов

---

## Карта

- Движок: **MapLibre GL JS 4.7.1** (open-source, без ключей)
- Тайлы: **CARTO Basemaps** `voyager` (бесплатно, без регистрации)
- Офлайн-позиции (`office`, `hybrid`) - маркер по точному адресу
- Удалённые (`remote`, `online`) - маркер по городу работодателя
- Клик по маркеру - попап с названием, компанией, зарплатой, тегами и кнопкой перехода
- На форме создания вакансии - клик по карте устанавливает координаты в скрытые поля

---

## Кастомные template tags

Файл: `apps/core/templatetags/tramplin_tags.py`  
Подключение: `{% load tramplin_tags %}` (обязательно в шаблонах, использующих эти фильтры)

| Фильтр | Использование | Описание |
|---|---|---|
| `split_skills` | `{{ user.skills\|split_skills }}` | Разбивает строку навыков по запятой, возвращает список |
| `trim` | `{{ value\|trim }}` | Обрезает пробелы по краям строки |

---

## Management Commands

| Команда | Описание | Идемпотентна |
|---|---|---|
| `create_initial_data` | Создаёт `admin@tramplin.kz` + 60+ системных тегов | ✅ Да |
| `create_demo_data` | 6 компаний, 16 вакансий, 8 соискателей с городами, отклики, контакты | ✅ Да |

```bash
python manage.py create_initial_data
python manage.py create_demo_data
```

> `create_demo_data` всегда сбрасывает пароли тестовых аккаунтов на `Demo12345!`

---

## Переменные окружения

| Переменная | Описание | По умолчанию |
|---|---|---|
| `DJANGO_SECRET_KEY` | Секретный ключ | `dev-secret-key` (**сменить в продакшене!**) |
| `DJANGO_DEBUG` | Режим отладки | `1` |
| `DJANGO_ALLOWED_HOSTS` | Разрешённые хосты (через запятую) | `127.0.0.1,localhost` |
| `DB_ENGINE` | `sqlite` или `postgres` | `sqlite` |
| `POSTGRES_DB` | Имя БД | `tramplin_db` |
| `POSTGRES_USER` | Пользователь БД | `tramplin_user` |
| `POSTGRES_PASSWORD` | Пароль БД | `tramplin_password` |
| `POSTGRES_HOST` | Хост БД | `127.0.0.1` |
| `POSTGRES_PORT` | Порт БД | `5432` |

---

## Требования (requirements.txt)

```
Django==5.2.1
djangorestframework==3.16.0
python-dotenv==1.1.0
psycopg[binary]==3.2.9
Pillow==10.4.0
```

---

## Примечания

- Карта работает **без API-ключей** - MapLibre GL (open-source) + CARTO Basemaps (бесплатно)
- Вакансии без координат (latitude/longitude) **не отображаются на карте**, но есть в списке
- После создания вакансии она попадает на модерацию (`is_moderated=False`) и **не видна** соискателям до одобрения
- Верификация компании - куратор проверяет корп. почту и ИНН вручную; без верификации работодатель не может создавать вакансии
- Контакты между соискателями: заявка → принятие с обеих сторон; без принятия связь не устанавливается
- Соискатели с `profile_public=False` **не отображаются** в каталоге специалистов
