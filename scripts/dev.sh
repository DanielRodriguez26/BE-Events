#!/bin/bash

# Development helper script for BE-Events

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker Desktop first."
        exit 1
    fi
}

# Function to check if containers are running
check_containers() {
    if docker-compose ps | grep -q "Up"; then
        return 0
    else
        return 1
    fi
}

# Function to start development environment
start_dev() {
    print_status "Starting development environment..."
    check_docker
    
    if check_containers; then
        print_warning "Containers are already running. Stopping them first..."
        docker-compose -f docker-compose.dev.yml down
    fi
    
    docker-compose -f docker-compose.dev.yml up --build -d
    print_success "Development environment started!"
    
    # Wait for services to be ready
    print_status "Waiting for services to be ready..."
    sleep 10
    
    # Check health
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_success "Application is healthy!"
    else
        print_warning "Application health check failed. Check logs with 'make logs'"
    fi
    
    print_status "Access points:"
    echo "  - Application: http://localhost:8000"
    echo "  - API Docs: http://localhost:8000/docs"
    echo "  - Database: localhost:5432"
    echo "  - Redis: localhost:6379"
}

# Function to stop development environment
stop_dev() {
    print_status "Stopping development environment..."
    docker-compose -f docker-compose.dev.yml down
    print_success "Development environment stopped!"
}

# Function to restart development environment
restart_dev() {
    print_status "Restarting development environment..."
    stop_dev
    start_dev
}

# Function to show logs
show_logs() {
    print_status "Showing application logs..."
    docker-compose -f docker-compose.dev.yml logs -f app
}

# Function to run tests
run_tests() {
    print_status "Running tests..."
    docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
}

# Function to run database migrations
run_migrations() {
    print_status "Running database migrations..."
    docker-compose -f docker-compose.dev.yml exec app alembic upgrade head
    print_success "Migrations completed!"
}

# Function to seed database
seed_database() {
    print_status "Seeding database..."
    docker-compose -f docker-compose.dev.yml exec app python seed_database.py
    print_success "Database seeded!"
}

# Function to reset database
reset_database() {
    print_warning "This will reset the database. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_status "Resetting database..."
        docker-compose -f docker-compose.dev.yml exec app alembic downgrade base
        docker-compose -f docker-compose.dev.yml exec app alembic upgrade head
        docker-compose -f docker-compose.dev.yml exec app python seed_database.py
        print_success "Database reset completed!"
    else
        print_status "Database reset cancelled."
    fi
}

# Function to show status
show_status() {
    print_status "Container status:"
    docker-compose -f docker-compose.dev.yml ps
    
    echo ""
    print_status "Service health:"
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_success "Application: Healthy"
    else
        print_error "Application: Unhealthy"
    fi
    
    if docker-compose -f docker-compose.dev.yml exec postgres pg_isready -U events_user -d events_db > /dev/null 2>&1; then
        print_success "Database: Healthy"
    else
        print_error "Database: Unhealthy"
    fi
    
    if docker-compose -f docker-compose.dev.yml exec redis redis-cli ping > /dev/null 2>&1; then
        print_success "Redis: Healthy"
    else
        print_error "Redis: Unhealthy"
    fi
}

# Function to show help
show_help() {
    echo "🚀 BE-Events Development Helper"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start     - Start development environment"
    echo "  stop      - Stop development environment"
    echo "  restart   - Restart development environment"
    echo "  logs      - Show application logs"
    echo "  test      - Run tests"
    echo "  migrate   - Run database migrations"
    echo "  seed      - Seed database"
    echo "  reset     - Reset database (with confirmation)"
    echo "  status    - Show container and service status"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 logs"
    echo "  $0 test"
}

# Main script logic
case "${1:-help}" in
    start)
        start_dev
        ;;
    stop)
        stop_dev
        ;;
    restart)
        restart_dev
        ;;
    logs)
        show_logs
        ;;
    test)
        run_tests
        ;;
    migrate)
        run_migrations
        ;;
    seed)
        seed_database
        ;;
    reset)
        reset_database
        ;;
    status)
        show_status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
