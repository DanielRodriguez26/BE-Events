# Makefile for BE-Events Docker operations

.PHONY: help setup dev prod test clean logs shell db-shell redis-shell build push

# Default target
help:
	@echo "🚀 BE-Events Docker Commands"
	@echo ""
	@echo "📋 Setup & Configuration:"
	@echo "  setup     - Initial Docker setup (generate SSL, create .env)"
	@echo "  build     - Build all Docker images"
	@echo ""
	@echo "🏃‍♂️ Run Environments:"
	@echo "  dev       - Start development environment"
	@echo "  prod      - Start production environment"
	@echo "  test      - Run tests in Docker"
	@echo ""
	@echo "🔧 Management:"
	@echo "  logs      - Show application logs"
	@echo "  shell     - Access application container shell"
	@echo "  db-shell  - Access PostgreSQL shell"
	@echo "  redis-shell - Access Redis shell"
	@echo "  clean     - Stop and remove all containers"
	@echo "  clean-all - Stop, remove containers and delete volumes"
	@echo ""
	@echo "📊 Database:"
	@echo "  migrate   - Run database migrations"
	@echo "  seed      - Seed database with initial data"
	@echo "  reset-db  - Reset database (drop and recreate)"

# Setup
setup:
	@echo "🔧 Setting up Docker environment..."
	@chmod +x scripts/docker-setup.sh
	@./scripts/docker-setup.sh

# Build
build:
	@echo "🔨 Building Docker images..."
	docker-compose build

# Development
dev:
	@echo "🚀 Starting development environment..."
	docker-compose -f docker-compose.dev.yml up --build

dev-detached:
	@echo "🚀 Starting development environment in background..."
	docker-compose -f docker-compose.dev.yml up --build -d

# Production
prod:
	@echo "🚀 Starting production environment..."
	docker-compose up --build

prod-detached:
	@echo "🚀 Starting production environment in background..."
	docker-compose up --build -d

# Testing
test:
	@echo "🧪 Running tests..."
	docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit

test-coverage:
	@echo "🧪 Running tests with coverage..."
	docker-compose -f docker-compose.test.yml run --rm test pytest tests/ -v --cov=app --cov-report=html --cov-report=term

# Management
logs:
	@echo "📋 Showing application logs..."
	docker-compose logs -f app

shell:
	@echo "🐚 Accessing application shell..."
	docker-compose exec app /bin/bash

db-shell:
	@echo "🐚 Accessing PostgreSQL shell..."
	docker-compose exec postgres psql -U events_user -d events_db

redis-shell:
	@echo "🐚 Accessing Redis shell..."
	docker-compose exec redis redis-cli

# Cleanup
clean:
	@echo "🧹 Stopping and removing containers..."
	docker-compose down

clean-all:
	@echo "🧹 Stopping, removing containers and deleting volumes..."
	docker-compose down -v
	docker system prune -f

# Database operations
migrate:
	@echo "🗄️ Running database migrations..."
	docker-compose exec app alembic upgrade head

seed:
	@echo "🌱 Seeding database..."
	docker-compose exec app python seed_database.py

reset-db:
	@echo "🔄 Resetting database..."
	docker-compose exec app alembic downgrade base
	docker-compose exec app alembic upgrade head
	docker-compose exec app python seed_database.py

# Health checks
health:
	@echo "🏥 Checking service health..."
	@curl -f http://localhost:8000/health || echo "❌ Application not healthy"
	@docker-compose exec postgres pg_isready -U events_user -d events_db || echo "❌ Database not healthy"
	@docker-compose exec redis redis-cli ping || echo "❌ Redis not healthy"

# Development helpers
format:
	@echo "🎨 Formatting code..."
	docker-compose exec app black app/ tests/

lint:
	@echo "🔍 Linting code..."
	docker-compose exec app flake8 app/ tests/

type-check:
	@echo "🔍 Type checking..."
	docker-compose exec app mypy app/

# Quick commands
restart:
	@echo "🔄 Restarting services..."
	docker-compose restart

status:
	@echo "📊 Service status:"
	docker-compose ps
