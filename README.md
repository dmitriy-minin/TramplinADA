# 🚀 Трамплин — Карьерная платформа для IT

Полнофункциональная платформа для централизованного взаимодействия студентов, выпускников, работодателей и кураторов вузов в сфере IT.

**Стек:** Python 3.11+, Django 5.2, Django REST Framework, PostgreSQL / SQLite, Leaflet.js

---

## Быстрый старт

### Вариант 1: Docker (рекомендуется)

```bash
cp .env.example .env
docker compose up --build
```

После запуска:
- http://127.0.0.1:8000/ — главная страница
- http://127.0.0.1:8000/api/health/ — health check

### Вариант 2: Локально (SQLite, без Docker)

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cd backend
python manage.py migrate
python manage.py create_initial_data
python manage.py create_demo_data   # опционально — тестовые данные
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

## Аккаунты по умолчанию

После `create_initial_data`:

| Роль | Email | Пароль |
|---|---|---|
| Администратор (куратор) | admin@tramplin.kz | Admin123!@# |

После `create_demo_data` (дополнительно):
Для всех тестовых аккаунтов пароль "Demo12345!".

| Роль | Email | Пароль |
|---|---|---|
| Работодатель | hr@kaspi-demo.kz | Demo12345! |
| Соискатель | aiya.bekova@demo.kz | Demo12345! |

Список работодателей: hr@kaspi-demo.kz, hr@kolesa-demo.kz, hr@epam-demo.kz, hr@smartec-demo.kz, hr@jusan-demo.kz, hr@startupkz-demo.kz.<br>
Список соискателей: aiya.bekova@demo.kz, arman.seitkali@demo.kz, dana.nurlan@demo.kz, timur.rakhimov@demo.kz, zhansaya.omar@demo.kz, bekzat.akhmet@demo.kz, alina.kim@demo.kz, ruslan.dyusembaev@demo.kz.

---

## Структура проекта

```
TramplinADA/
├── backend/
│   ├── apps/
│   │   ├── accounts/        # Пользователи: соискатели и работодатели
│   │   ├── companies/       # Компании и верификация
│   │   ├── opportunities/   # Вакансии, стажировки, мероприятия, отклики
│   │   ├── curator/         # Панель куратора платформы
│   │   └── core/            # Главная страница, management commands
│   ├── config/              # Settings, URLs, WSGI/ASGI
│   ├── templates/           # HTML-шаблоны (Django templates)
│   ├── static/
│   │   ├── css/main.css     # Дизайн-система (~700 строк)
│   │   └── js/main.js       # Клиентская логика
│   └── scripts/entrypoint.sh
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## Маршруты (URL)

| URL | Описание |
|---|---|
| `/` | Главная: карта + список вакансий |
| `/opportunities/` | Все вакансии с фильтрами |
| `/opportunities/<id>/` | Детали вакансии + форма отклика |
| `/auth/login/` | Вход |
| `/auth/register/` | Выбор роли при регистрации |
| `/auth/register/applicant/` | Регистрация соискателя |
| `/auth/register/employer/` | Регистрация работодателя |
| `/dashboard/` | Редирект в нужный кабинет |
| `/dashboard/applicant/` | Кабинет соискателя |
| `/dashboard/applicant/profile/` | Редактирование профиля |
| `/dashboard/employer/` | Кабинет работодателя |
| `/dashboard/employer/create/` | Создать вакансию |
| `/dashboard/employer/<id>/applicants/` | Отклики на вакансию |
| `/curator/` | Панель куратора |
| `/curator/companies/` | Верификация компаний |
| `/curator/opportunities/` | Модерация вакансий |
| `/curator/users/` | Управление пользователями |
| `/curator/tags/` | Управление тегами |
| `/curator/curators/` | Создание кураторов (только admin) |
| `/profile/<id>/` | Публичный профиль соискателя |
| `/api/map-markers/` | GeoJSON маркеры для карты |

---

## Модели данных

### User (accounts)
- Роли: `applicant` | `employer` | `curator`
- Поля соискателя: ФИО, вуз, год выпуска, навыки, опыт, GitHub, портфолио, резюме
- Приватность: `profile_public`, `hide_applications`
- Контакты: M2M (`contacts`) + заявки (`contact_requests`)

### Company (companies)
- Верификация: `pending` → `verified` | `rejected`
- Поля: название, отрасль, описание, сайт, LinkedIn, Telegram, HH, корп. почта, ИНН

### Tag (opportunities)
- Типы: `skill` (Python, React...) | `level` (Junior, Middle...) | `employment` (полная, частичная...)
- 60+ системных тегов создаются командой `create_initial_data`

### Opportunity (opportunities)
- Типы: `internship` | `vacancy` | `mentoring` | `event`
- Форматы: `office` | `hybrid` | `remote` | `online`
- Статусы: `active` | `closed` | `planned` | `draft`
- Геолокация: `latitude`, `longitude` для карты Leaflet
- Модерация: `is_moderated` (куратор одобряет перед публикацией)

### Application (opportunities)
- Статусы: `pending` → `accepted` | `rejected` | `reserve`
- Поле `is_favorite` для избранного

---

## Функциональность

### Публичная часть (неавторизованные)
- Просмотр вакансий на карте (Leaflet + OpenStreetMap)
- Просмотр в виде сетки или списка
- Фильтрация: тип, формат, навыки, зарплата, город
- Детальная страница вакансии

### Соискатель
- Регистрация → профиль с резюме и навыками
- Отклик на вакансию с сопроводительным письмом
- Избранное (сохранить вакансию)
- История откликов + статусы ответов
- Публичный профиль с настройками приватности
- Профессиональные контакты (нетворкинг)

### Работодатель
- Регистрация + создание компании → верификация куратором
- Создание и редактирование вакансий/мероприятий
- Выбор координат прямо на карте при создании
- Управление откликами: принять / отклонить / в резерв
- Просмотр профилей и резюме соискателей

### Куратор
- Верификация компаний (проверка корп. почты, ИНН)
- Модерация вакансий (одобрить / отклонить с примечанием)
- Управление пользователями (блокировка)
- Управление тегами (создание / удаление)
- Только администратор может создавать других кураторов

---

## Изменения относительно Stage 1 (исходный каркас)

| Компонент | Stage 1 | Stage 2 |
|---|---|---|
| Модели | — | User, Company, Tag, Opportunity, Application, CuratorProfile |
| AUTH_USER_MODEL | стандартный | кастомный `accounts.User` с ролями |
| БД | SQLite (жёстко) | SQLite + PostgreSQL через `DB_ENGINE` |
| Шаблонов | 1 (заглушка) | 23 полных HTML-шаблона |
| CSS | 15 строк | 700+ строк дизайн-системы |
| JS | — | main.js + Leaflet.js |
| URL-маршрутов | 3 | 25+ |
| Management commands | — | `create_initial_data`, `create_demo_data` |
| API | — | `/api/map-markers/` |
| Пользователи | — | Регистрация, вход, 3 роли |

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

## Примечания для разработки

- Карта использует **OpenStreetMap** через **Leaflet.js** (без API-ключа)
- Геокодирование адресов: клик по карте при создании вакансии устанавливает координаты
- Вакансии без координат не отображаются на карте
- Для офлайн-формата (`office`, `hybrid`) отображается точный адрес; для удалённых — город работодателя
- Верификация компании: куратор проверяет корпоративную почту и/или ИНН вручную
- После создания вакансии работодателем она попадает на модерацию (статус `is_moderated=False`)
