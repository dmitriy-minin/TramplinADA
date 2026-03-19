# ============================================================
# Трамплин — Makefile
# Команды для удобного управления проектом
# ============================================================

.PHONY: help dev-backend dev-frontend install-backend install-frontend \
        docker-up docker-down docker-logs seed lint type-check

help: ## Показать список команд
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ─── Локальная разработка ────────────────────────────────────

install-backend: ## Установить зависимости backend
	cd backend && pip install -r requirements.txt

install-frontend: ## Установить зависимости frontend
	cd frontend && npm install

install: install-backend install-frontend ## Установить все зависимости

dev-backend: ## Запустить backend в режиме разработки
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Запустить frontend в режиме разработки
	cd frontend && npm run dev

seed: ## Заполнить БД начальными тегами
	cd backend && python seed_tags.py

# ─── Docker ──────────────────────────────────────────────────

docker-up: ## Запустить всё через Docker Compose
	docker compose up --build -d
	@echo ""
	@echo "✅ Запущено!"
	@echo "   Frontend: http://localhost:5173"
	@echo "   Backend:  http://localhost:8000"
	@echo "   API docs: http://localhost:8000/api/docs"

docker-down: ## Остановить Docker Compose
	docker compose down

docker-reset: ## Остановить и удалить все данные
	docker compose down -v --remove-orphans

docker-logs: ## Показать логи
	docker compose logs -f

docker-logs-backend: ## Логи только backend
	docker compose logs -f backend

# ─── Качество кода ───────────────────────────────────────────

lint-frontend: ## Линтинг frontend
	cd frontend && npm run lint

type-check: ## Проверка типов TypeScript
	cd frontend && npm run type-check

build-frontend: ## Сборка frontend для production
	cd frontend && npm run build
