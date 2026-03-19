#!/usr/bin/env bash
# ============================================================
# Трамплин — Quick Start Script
# Запускает проект через Docker Compose
# ============================================================

set -e

echo ""
echo "  🚀  Трамплин — Quick Start"
echo "================================"
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌  Docker не найден. Установите Docker Desktop: https://docker.com"
    exit 1
fi

if ! docker compose version &> /dev/null; then
    echo "❌  Docker Compose не найден."
    exit 1
fi

# Create .env if not exists
if [ ! -f backend/.env ]; then
    echo "📋  Создаём backend/.env из шаблона..."
    cp backend/.env.example backend/.env
    echo "✅  backend/.env создан"
fi

echo ""
echo "🔨  Сборка и запуск контейнеров..."
echo ""

docker compose up --build -d

echo ""
echo "⏳  Ожидание запуска сервисов..."
sleep 10

echo ""
echo "✅  Трамплин запущен!"
echo ""
echo "  🌐  Frontend:  http://localhost:5173"
echo "  🔧  Backend:   http://localhost:8000"
echo "  📚  API Docs:  http://localhost:8000/api/docs"
echo ""
echo "  👤  Администратор:"
echo "      Email:    admin@tramplin.kz"
echo "      Пароль:   Admin123!@#"
echo ""
echo "  📊  Логи:  docker compose logs -f"
echo "  🛑  Стоп:  docker compose down"
echo ""
