# 🚀 Трамплин — платформа для IT-карьеры (текущая версия 0.1)

**Трамплин** — веб-платформа, объединяющая студентов/выпускников IT-вузов, работодателей и кураторов. Вакансии, стажировки, менторские программы и карьерные мероприятия.

---

## 📋 Содержание

- [Стек технологий](#стек-технологий)
- [Архитектура](#архитектура)
- [Файловая структура](#файловая-структура)
- [Необходимое ПО](#необходимое-по)
- [Быстрый старт](#быстрый-старт)
- [Настройка окружения](#настройка-окружения)
- [Запуск в разработке](#запуск-в-разработке)
- [Запуск через Docker](#запуск-через-docker)
- [API документация](#api-документация)
- [Роли пользователей](#роли-пользователей)
- [Безопасность](#безопасность)

---

## 🛠 Стек технологий

### Backend
| Технология | Версия | Назначение |
|---|---|---|
| Python | 3.11 | Язык программирования |
| FastAPI | 0.115 | Веб-фреймворк, REST API |
| SQLAlchemy | 2.0 | ORM (async) |
| asyncpg | 0.29 | Асинхронный драйвер PostgreSQL |
| Alembic | 1.13 | Миграции БД |
| Pydantic v2 | 2.9 | Валидация данных, схемы |
| python-jose | 3.3 | JWT токены |
| passlib + bcrypt | 1.7 | Хеширование паролей |
| Resend | 2.4 | Email-уведомления |
| Cloudinary | 1.41 | Хранение медиафайлов |

### Frontend
| Технология | Версия | Назначение |
|---|---|---|
| React | 18.3 | UI-библиотека |
| TypeScript | 5.5 | Типизация |
| Vite | 5.4 | Сборщик |
| TailwindCSS | 3.4 | CSS-фреймворк |
| React Router | 6.26 | Маршрутизация |
| TanStack Query | 5.56 | Кеширование и синхронизация данных |
| Zustand | 5.0 | Глобальное состояние |
| React Hook Form | 7.53 | Формы |
| Zod | 3.23 | Валидация схем |
| Leaflet | 1.9 | Интерактивная карта (OpenStreetMap) |
| Axios | 1.7 | HTTP клиент |
| react-hot-toast | 2.4 | Уведомления |
| Lucide React | 0.447 | Иконки |

### Инфраструктура
| Технология | Назначение |
|---|---|
| PostgreSQL 16 | Основная БД |
| Docker + Docker Compose | Контейнеризация |
| Nginx | Reverse proxy, отдача статики |
| OpenStreetMap + Nominatim | Карта и геокодинг (бесплатно) |

---

## 🏗 Архитектура

```
┌─────────────────────────────────────────────────────────────────┐
│                         КЛИЕНТ (браузер)                        │
│              React + Vite + TypeScript + TailwindCSS            │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTPS / HTTP
┌──────────────────────────────▼──────────────────────────────────┐
│                     Nginx (reverse proxy)                       │
│            /api/* → backend:8000   /* → static SPA             │
└──────────┬──────────────────────────┬───────────────────────────┘
           │                          │
┌──────────▼──────────┐    ┌──────────▼──────────────────────────┐
│   FastAPI Backend   │    │       Frontend Static (dist/)        │
│  Python 3.11        │    │   HTML + JS + CSS bundle             │
│  ├─ Routers         │    └─────────────────────────────────────┘
│  ├─ Services        │
│  ├─ Models          │    External services:
│  ├─ Schemas         │    ┌─────────────────┐
│  └─ Core/Security   │    │  Cloudinary     │ (медиафайлы)
└──────────┬──────────┘    ├─────────────────┤
           │               │  Resend         │ (email)
┌──────────▼──────────┐    ├─────────────────┤
│   PostgreSQL 16     │    │  OpenStreetMap  │ (карта)
│   ├─ users          │    └─────────────────┘
│   ├─ companies      │
│   ├─ opportunities  │
│   ├─ applications   │
│   ├─ tags           │
│   ├─ contacts       │
│   └─ favorites      │
└─────────────────────┘
```

### Принципы архитектуры Backend

- **Layered architecture**: Routes → Services → Models → DB
- **Dependency Injection** через FastAPI `Depends()`
- **Async everywhere**: все операции с БД асинхронные
- **JWT + Refresh tokens**: безопасная аутентификация
- **Role-based access control (RBAC)**: soiskatel / employer / curator
- **Pydantic v2** для строгой валидации входящих данных

---

## 📁 Файловая структура

```
tramplin/
├── 📄 docker-compose.yml          # Оркестрация контейнеров
├── 📄 README.md
│
├── 📂 backend/
│   ├── 📄 Dockerfile
│   ├── 📄 requirements.txt
│   ├── 📄 .env.example
│   └── 📂 app/
│       ├── 📄 main.py             # Точка входа FastAPI
│       ├── 📂 api/
│       │   └── 📂 v1/
│       │       ├── 📄 router.py   # Главный роутер
│       │       └── 📂 endpoints/
│       │           ├── 📄 auth.py           # /auth/*
│       │           ├── 📄 opportunities.py  # /opportunities/*
│       │           └── 📄 misc.py           # /tags, /applications, /favorites, /users, /companies
│       ├── 📂 core/
│       │   ├── 📄 config.py       # Настройки (pydantic-settings)
│       │   ├── 📄 security.py     # JWT, bcrypt, валидация пароля
│       │   └── 📄 deps.py         # FastAPI Dependencies
│       ├── 📂 db/
│       │   └── 📄 database.py     # SQLAlchemy engine, session, seed
│       ├── 📂 models/
│       │   ├── 📄 user.py         # User, UserRole, PrivacyLevel
│       │   ├── 📄 company.py      # Company
│       │   ├── 📄 opportunity.py  # Opportunity, Tag, many-to-many
│       │   └── 📄 application.py  # Application, Contact, Favorite
│       └── 📂 schemas/
│           ├── 📄 user.py         # Pydantic схемы пользователя
│           └── 📄 opportunity.py  # Pydantic схемы вакансий
│
└── 📂 frontend/
    ├── 📄 Dockerfile
    ├── 📄 nginx.conf
    ├── 📄 package.json
    ├── 📄 vite.config.ts
    ├── 📄 tailwind.config.js
    ├── 📄 tsconfig.json
    ├── 📄 index.html
    └── 📂 src/
        ├── 📄 main.tsx            # Точка входа React
        ├── 📄 App.tsx             # Роутер
        ├── 📄 index.css           # Глобальные стили + Tailwind
        ├── 📂 types/
        │   └── 📄 index.ts        # TypeScript типы
        ├── 📂 lib/
        │   └── 📄 api.ts          # Axios + interceptors
        ├── 📂 store/
        │   └── 📄 auth.ts         # Zustand auth store
        ├── 📂 components/
        │   ├── 📂 common/
        │   │   └── 📄 Navbar.tsx
        │   ├── 📂 opportunities/
        │   │   ├── 📄 OpportunityCard.tsx
        │   │   └── 📄 OpportunityFilters.tsx
        │   └── 📂 map/
        │       └── 📄 MapView.tsx  # Leaflet карта
        └── 📂 pages/
            ├── 📄 LandingPage.tsx
            ├── 📄 LoginPage.tsx
            ├── 📄 RegisterPage.tsx
            ├── 📄 OpportunitiesPage.tsx
            ├── 📄 OpportunityDetailPage.tsx
            └── 📂 dashboard/
                ├── 📄 DashboardLayout.tsx
                ├── 📄 DashboardHome.tsx
                ├── 📄 ProfilePage.tsx
                ├── 📄 MyApplications.tsx
                ├── 📄 MyOpportunities.tsx
                ├── 📄 CreateOpportunity.tsx
                └── 📄 AdminPanel.tsx
```

---

## 💻 Необходимое ПО

| ПО | Минимальная версия | Скачать |
|---|---|---|
| **Node.js** | 20.x LTS | https://nodejs.org |
| **npm** | 10.x (идёт с Node.js) | — |
| **Python** | 3.11+ | https://python.org |
| **pip** | 23+ | идёт с Python |
| **PostgreSQL** | 15+ | https://postgresql.org |
| **Docker** | 24+ | https://docker.com |
| **Docker Compose** | 2.20+ | идёт с Docker Desktop |
| **Git** | 2.x | https://git-scm.com |

> **Примечание**: Для запуска через Docker нужен только Docker и Docker Compose. Python, Node.js и PostgreSQL нужны только для локальной разработки без Docker.

---

## ⚡ Быстрый старт

### Вариант 1: Docker Compose (рекомендуется)

```bash
# 1. Клонируй репозиторий
git clone https://github.com/your-org/tramplin.git
cd tramplin

# 2. Создай .env файл для backend
cp backend/.env.example backend/.env

# 3. При необходимости отредактируй backend/.env (настройки по умолчанию работают)

# 4. Запусти всё одной командой
docker compose up --build

# Приложение будет доступно:
# Frontend:  http://localhost:5173
# Backend:   http://localhost:8000
# API docs:  http://localhost:8000/api/docs
```

---

### Вариант 2: Локальная разработка

#### 2.1 Настройка базы данных

```bash
# Создай базу данных в PostgreSQL
psql -U postgres -c "CREATE DATABASE tramplin;"
```

#### 2.2 Настройка и запуск Backend

> ⚠️ **Важно**: uvicorn нужно запускать **из папки `backend/`**, иначе Python не найдёт модуль `app`.

```bash
# Перейди в папку backend (ОБЯЗАТЕЛЬНО!)
cd backend

# Создай виртуальное окружение
python -m venv .venv

# Активируй (Linux/Mac):
source .venv/bin/activate
# или Windows:
.venv\Scripts\activate

# Установи зависимости
pip install -r requirements.txt

# Создай .env файл
cp .env.example .env
# Отредактируй .env (минимум: DATABASE_URL)

# Запусти сервер (находясь в папке backend/)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Или используй готовый скрипт:
bash run.sh

# Backend будет на: http://localhost:8000
# Swagger UI:       http://localhost:8000/api/docs
```

> Если хочешь запускать из корня проекта:
> ```bash
> PYTHONPATH=backend uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
> ```

#### 2.3 Настройка и запуск Frontend

```bash
cd frontend

# Для Linux
sudo apt install nodejs npm

# Установи зависимости
npm install

# Запусти dev-сервер
npm run dev

# Frontend будет на: http://localhost:5173
```

---

## ⚙️ Настройка окружения

Скопируй `backend/.env.example` в `backend/.env` и заполни:

```env
# Обязательные настройки
SECRET_KEY=your-super-secret-key-at-least-32-chars   # Любая случайная строка
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/tramplin

# Администратор (создаётся автоматически при первом запуске)
ADMIN_EMAIL=admin@tramplin.kz
ADMIN_PASSWORD=Admin123!@#    # Минимум 8 символов, заглавная, цифра
ADMIN_NAME=Главный администратор

# Опционально — Email уведомления (Resend)
RESEND_API_KEY=re_xxxx        # Получить на https://resend.com

# Опционально — Хранение файлов (Cloudinary)
CLOUDINARY_CLOUD_NAME=xxx
CLOUDINARY_API_KEY=xxx
CLOUDINARY_API_SECRET=xxx
```

---

## 🔑 Учётные данные по умолчанию

После первого запуска создаётся главный администратор:

| Поле | Значение |
|---|---|
| Email | `admin@tramplin.kz` |
| Пароль | `Admin123!@#` |
| Роль | Куратор (главный администратор) |

> ⚠️ **Важно**: Смените пароль администратора после первого входа в production!

---

## 📡 API документация

После запуска backend документация доступна по адресам:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Основные эндпоинты

| Метод | URL | Описание |
|---|---|---|
| POST | `/api/v1/auth/register` | Регистрация |
| POST | `/api/v1/auth/login` | Вход |
| POST | `/api/v1/auth/refresh` | Обновление токена |
| GET | `/api/v1/auth/me` | Текущий пользователь |
| GET | `/api/v1/opportunities` | Список вакансий (с фильтрами) |
| GET | `/api/v1/opportunities/{id}` | Карточка вакансии |
| POST | `/api/v1/opportunities` | Создать вакансию (employer) |
| POST | `/api/v1/opportunities/{id}/moderate` | Модерировать (curator) |
| GET | `/api/v1/tags` | Список тегов |
| POST | `/api/v1/applications` | Откликнуться |
| GET | `/api/v1/applications/my` | Мои отклики |
| POST | `/api/v1/favorites/{id}` | Добавить в избранное |
| GET | `/api/v1/companies` | Список компаний (curator) |
| PATCH | `/api/v1/companies/{id}/verify` | Верифицировать компанию |

---

## 👥 Роли пользователей

### 🎓 Соискатель (soiskatel)
- Просмотр всех активных вакансий на карте и в ленте
- Отклики на вакансии с сопроводительным письмом
- Профиль с резюме в Markdown, GitHub, портфолио
- Избранные вакансии
- Настройка приватности резюме

### 🏢 Работодатель (employer)
- Создание карточек возможностей (вакансии, стажировки, менторство, мероприятия)
- Управление откликами (принять / отклонить / в резерв)
- Профиль компании с логотипом и описанием
- Верификация куратором перед публикацией

### 🛡️ Куратор / Администратор (curator)
- Модерация карточек (одобрить / отклонить)
- Верификация компаний
- Управление пользователями
- Управление тегами технологий
- Главный администратор может создавать других кураторов

---

## 🔐 Безопасность

- **Пароли**: хешируются через bcrypt (cost factor 12)
- **JWT**: access token (30 мин) + refresh token (7 дней)
- **CORS**: настроен список разрешённых origins
- **Валидация**: Pydantic v2 на всех входящих данных
- **RBAC**: все защищённые эндпоинты проверяют роль через `Depends()`
- **SQL Injection**: защита через SQLAlchemy ORM (параметризованные запросы)
- **XSS**: React экранирует контент по умолчанию
- **Trusted Hosts**: middleware для проверки заголовка Host

---

## 🐛 Решение проблем

**Порт уже занят:**
```bash
# Проверь что использует порт
lsof -i :8000  # или :5432, :5173
```

**Ошибка подключения к БД:**
```bash
# Убедись что PostgreSQL запущен
pg_isready -h localhost -p 5432
```

**Ошибка при установке Python зависимостей:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Пересборка Docker контейнеров:**
```bash
docker compose down -v  # удалить тома с данными
docker compose up --build --force-recreate
```

---

## 📝 Дополнительные команды

```bash
# Backend тесты (при наличии)
cd backend && pytest

# Проверка типов Frontend
cd frontend && npm run type-check

# Линтинг Frontend
cd frontend && npm run lint

# Сборка Frontend для production
cd frontend && npm run build

# Просмотр логов Docker
docker compose logs -f backend
docker compose logs -f db

# Подключение к БД в Docker
docker compose exec db psql -U postgres -d tramplin
```

---

## 🤝 Контакты

Проект разработан для конкурса. По вопросам обращайтесь к команде разработчиков.
Разработчики: Минин Дмитрий, Айджан Амалия, Максутов Азамат.
Студенты 1 курса магистратуры ЗКАТУ им. Жангир хана, город Уральск, Западно-Казахстанская область.

---

